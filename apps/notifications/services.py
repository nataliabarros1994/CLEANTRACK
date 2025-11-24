"""
Email notification services using Resend API
"""
import os
import resend
import logging
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

# Configure Resend API key
resend.api_key = settings.RESEND_API_KEY


def send_cleaning_alert(to_email: str, equipment_name: str):
    """
    Send an alert email when equipment cleaning is overdue

    Args:
        to_email: Recipient email address
        equipment_name: Name of the equipment that needs cleaning

    Returns:
        dict: Response from Resend API or None if failed
    """
    try:
        response = resend.Emails.send({
            "from": "CleanTrack Alerts <onboarding@resend.dev>",
            "to": to_email,
            "subject": f"⚠️ Limpeza atrasada: {equipment_name}",
            "html": f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h2 style="color: #e74c3c;">⚠️ Alerta de Limpeza Atrasada</h2>
                    <p>O equipamento <strong>{equipment_name}</strong> não foi limpo conforme o cronograma.</p>
                    <p>Por favor, realize a limpeza o mais breve possível para manter a conformidade.</p>
                    <hr>
                    <p style="color: #7f8c8d; font-size: 0.9em;">
                        Esta é uma mensagem automática do CleanTrack.<br>
                        Sistema de Gestão de Conformidade de Limpeza de Equipamentos Médicos
                    </p>
                </body>
            </html>
            """
        })
        logger.info(f"Alert email sent to {to_email} for equipment: {equipment_name}")
        return response
    except Exception as e:
        logger.error(f"Error sending alert email to {to_email}: {e}")
        return None


def send_compliance_summary(to_email: str, summary_data: dict):
    """
    Send weekly compliance summary email

    Args:
        to_email: Recipient email address
        summary_data: Dictionary with compliance data
            - total_equipment: int
            - cleanings_completed: int
            - overdue_count: int
            - compliance_rate: float

    Returns:
        dict: Response from Resend API or None if failed
    """
    try:
        compliance_rate = summary_data.get('compliance_rate', 0)
        total_equipment = summary_data.get('total_equipment', 0)
        cleanings_completed = summary_data.get('cleanings_completed', 0)
        overdue_count = summary_data.get('overdue_count', 0)

        response = resend.Emails.send({
            "from": "CleanTrack Reports <onboarding@resend.dev>",
            "to": to_email,
            "subject": "📊 Resumo Semanal de Conformidade - CleanTrack",
            "html": f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h2 style="color: #3498db;">📊 Resumo Semanal de Conformidade</h2>

                    <div style="background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0;">Estatísticas da Semana</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li>✓ <strong>Total de Equipamentos:</strong> {total_equipment}</li>
                            <li>✓ <strong>Limpezas Realizadas:</strong> {cleanings_completed}</li>
                            <li>⚠️ <strong>Equipamentos Atrasados:</strong> {overdue_count}</li>
                            <li>📈 <strong>Taxa de Conformidade:</strong> {compliance_rate:.1f}%</li>
                        </ul>
                    </div>

                    <p>Continue mantendo os altos padrões de conformidade!</p>

                    <hr>
                    <p style="color: #7f8c8d; font-size: 0.9em;">
                        CleanTrack - Sistema de Gestão de Conformidade<br>
                        Relatório gerado automaticamente
                    </p>
                </body>
            </html>
            """
        })
        logger.info(f"Compliance summary email sent to {to_email}")
        return response
    except Exception as e:
        logger.error(f"Error sending compliance summary to {to_email}: {e}")
        return None


def send_welcome_email(to_email: str, user_name: str):
    """
    Send welcome email to new users

    Args:
        to_email: Recipient email address
        user_name: Name of the new user

    Returns:
        dict: Response from Resend API or None if failed
    """
    try:
        response = resend.Emails.send({
            "from": "CleanTrack <onboarding@resend.dev>",
            "to": to_email,
            "subject": "Bem-vindo ao CleanTrack!",
            "html": f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h2 style="color: #27ae60;">Bem-vindo ao CleanTrack, {user_name}!</h2>

                    <p>Estamos felizes em tê-lo(a) conosco!</p>

                    <p>O CleanTrack ajudará você a:</p>
                    <ul>
                        <li>Gerenciar equipamentos médicos</li>
                        <li>Registrar atividades de limpeza</li>
                        <li>Garantir conformidade regulatória</li>
                        <li>Gerar relatórios de conformidade</li>
                    </ul>

                    <p>
                        <a href="http://localhost:8000/admin"
                           style="background: #3498db; color: white; padding: 10px 20px;
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Acessar Sistema
                        </a>
                    </p>

                    <hr>
                    <p style="color: #7f8c8d; font-size: 0.9em;">
                        CleanTrack - Garantindo conformidade, uma limpeza por vez.<br>
                        Dúvidas? Entre em contato conosco.
                    </p>
                </body>
            </html>
            """
        })
        logger.info(f"Welcome email sent to {to_email}")
        return response
    except Exception as e:
        logger.error(f"Error sending welcome email to {to_email}: {e}")
        return None


def notify_cleaning_registered(cleaning_log):
    """
    Envio opcional: notifica o gerente da unidade sobre nova limpeza.

    Estratégia de notificação:
    1. Primeiro tenta notificar gerentes específicos da facility
    2. Se não houver, notifica todos os managers/admins ativos
    3. Se ainda não houver, notifica superusuários

    Args:
        cleaning_log: CleaningLog instance

    Returns:
        dict: Response from Resend API or None if failed
    """
    try:
        facility = cleaning_log.equipment.facility

        # Estratégia 1: Gerentes específicos da facility
        facility_managers = User.objects.filter(
            managed_facilities=facility,
            is_active=True
        )

        if facility_managers.exists():
            managers = facility_managers
            logger.info(f"Notifying {managers.count()} facility-specific managers")
        else:
            # Estratégia 2: Todos os managers e admins
            managers = User.objects.filter(
                role__in=['admin', 'manager'],
                is_active=True
            )

            if managers.exists():
                logger.info(f"No facility managers found, notifying {managers.count()} general managers")
            else:
                # Estratégia 3: Fallback para superusuários
                managers = User.objects.filter(is_superuser=True, is_active=True)
                if managers.exists():
                    logger.info(f"No managers found, notifying {managers.count()} superusers as fallback")

        if not managers.exists():
            logger.warning("No managers, admins, or superusers found to notify about cleaning registration")
            return None

        subject = f"Nova limpeza registrada: {cleaning_log.equipment.name}"
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #27ae60;">Registro de Limpeza Confirmado</h2>
                <div style="background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Equipamento:</strong> {cleaning_log.equipment.name}</p>
                    <p><strong>Número de série:</strong> {cleaning_log.equipment.serial_number}</p>
                    <p><strong>Local:</strong> {cleaning_log.equipment.facility.name}</p>
                    <p><strong>Data:</strong> {cleaning_log.cleaned_at.strftime('%d/%m/%Y %H:%M')}</p>
                    <p><strong>Registrado por:</strong> {cleaning_log.cleaned_by.get_full_name() if cleaning_log.cleaned_by else 'Sistema'}</p>
                    <p><strong>Conformidade:</strong> {'Em conformidade' if cleaning_log.is_compliant else 'Fora do prazo'}</p>
                </div>
                <hr>
                <p style="color: #7f8c8d; font-size: 0.9em;">
                    Esta é uma mensagem automática do CleanTrack.<br>
                    Sistema de Gestão de Conformidade de Limpeza de Equipamentos Médicos
                </p>
            </body>
        </html>
        """

        emails = [user.email for user in managers if user.email]
        if not emails:
            logger.warning("No valid emails found among managers")
            return None

        response = resend.Emails.send({
            "from": "CleanTrack <onboarding@resend.dev>",
            "to": emails,
            "subject": subject,
            "html": html,
        })
        logger.info(f"Cleaning registration notification sent to {len(emails)} recipients")
        return response

    except Exception as e:
        logger.error(f"Error sending cleaning registration notification: {e}")
        return None
