from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email et mot de passe requis.")

        user = User.objects.filter(email__iexact=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError({"detail": "Identifiants invalides."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "Compte désactivé."})

        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "email"]


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
            send_mail(
                subject="Réinitialisation de votre mot de passe",
                message=f"Cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

        return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=False)
    token = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({"detail": "Les mots de passe ne correspondent pas."})

        validate_password(password)

        uid = attrs.get("uid")
        token = attrs.get("token")
        email = attrs.get("email")

        if not uid and not email:
            raise serializers.ValidationError({"detail": "Un identifiant utilisateur ou un email est requis."})

        if uid:
            try:
                user_id = force_str(urlsafe_base64_decode(uid))
            except (TypeError, ValueError, OverflowError):
                raise serializers.ValidationError({"detail": "UID invalide."})
            user = User.objects.filter(pk=user_id).first()
        else:
            user = User.objects.filter(email__iexact=email).first()

        if user is None:
            raise serializers.ValidationError({"detail": "Utilisateur introuvable."})

        if token and not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Token invalide ou expiré."})

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user
