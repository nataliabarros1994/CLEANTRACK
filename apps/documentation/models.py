"""
Models for Documentation app
"""
from django.db import models


class FeatureCategory(models.Model):
    """
    Categories for organizing features
    """
    name = models.CharField(
        "Nome da Categoria",
        max_length=100,
        unique=True,
        help_text="Ex: Equipamentos, QR Code, Limpeza"
    )
    slug = models.SlugField(
        "Slug",
        max_length=100,
        unique=True,
        help_text="URL-friendly version of name"
    )
    icon = models.CharField(
        "Ícone",
        max_length=20,
        blank=True,
        help_text="Emoji ou classe de ícone (ex: 🔧, fa-cog)"
    )
    description = models.TextField(
        "Descrição",
        blank=True,
        help_text="Breve descrição da categoria"
    )
    order = models.PositiveIntegerField(
        "Ordem",
        default=0,
        help_text="Ordem de exibição (menor = primeiro)"
    )
    is_active = models.BooleanField(
        "Ativo",
        default=True,
        help_text="Exibir esta categoria na documentação"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria de Funcionalidade"
        verbose_name_plural = "Categorias de Funcionalidades"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class Feature(models.Model):
    """
    Individual features/functionality documentation
    """
    BADGE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('public', 'Public'),
        ('security', 'Security'),
        ('api', 'API'),
        ('command', 'Command'),
        ('webhook', 'Webhook'),
        ('none', 'None'),
    ]

    category = models.ForeignKey(
        FeatureCategory,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name="Categoria"
    )
    name = models.CharField(
        "Nome da Funcionalidade",
        max_length=200,
        help_text="Ex: QR no Admin, PDF de Etiquetas"
    )
    description = models.TextField(
        "Como Usar",
        help_text="Instruções passo a passo de como usar esta funcionalidade"
    )
    endpoint = models.CharField(
        "Endpoint/Comando",
        max_length=300,
        blank=True,
        help_text="URL endpoint ou comando de gerenciamento (ex: /equipment/labels/pdf/<id>/, python manage.py ...)"
    )
    code_example = models.TextField(
        "Exemplo de Código",
        blank=True,
        help_text="Exemplo de código ou uso da funcionalidade"
    )
    badge = models.CharField(
        "Badge",
        max_length=20,
        choices=BADGE_CHOICES,
        default='none',
        help_text="Badge de classificação da funcionalidade"
    )
    is_featured = models.BooleanField(
        "Destaque",
        default=False,
        help_text="Marcar como funcionalidade em destaque"
    )
    requires_auth = models.BooleanField(
        "Requer Autenticação",
        default=False,
        help_text="Esta funcionalidade requer autenticação"
    )
    requires_permission = models.CharField(
        "Requer Permissão",
        max_length=100,
        blank=True,
        help_text="Permissão necessária (ex: admin, manager, manager_or_admin)"
    )
    order = models.PositiveIntegerField(
        "Ordem",
        default=0,
        help_text="Ordem de exibição dentro da categoria"
    )
    is_active = models.BooleanField(
        "Ativo",
        default=True,
        help_text="Exibir esta funcionalidade na documentação"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Funcionalidade"
        verbose_name_plural = "Funcionalidades"
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    @property
    def badge_display(self):
        """Get badge display text"""
        return dict(self.BADGE_CHOICES).get(self.badge, '')
