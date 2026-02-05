import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_templated_email(
    *,
    to_emails,
    subject,
    template_name,
    context,
    from_email=None,
):

    # 1. Đảm bảo to_emails luôn là một danh sách (List)
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    if not to_emails:
        logger.error("Không có email người nhận")
        raise ValueError("Missing recipient email")

    try:
        # 2. Render HTML template
        html_content = render_to_string(template_name, context)
        if not html_content.strip():
            raise ValueError(f"Template '{template_name}' render ra nội dung rỗng")

        text_content = strip_tags(html_content)

        # 3. Sử dụng trực tiếp email đã test thành công
        final_from_email = "taolink14@gmail.com"
        
        logger.info(f"Gửi từ: {final_from_email} đến: {to_emails}")

        # 4. Tạo email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=final_from_email,
            to=to_emails,
        )

        # 5. Đính kèm nội dung HTML
        msg.attach_alternative(html_content, "text/html")

        # 6. Thực hiện gửi
        sent = msg.send(fail_silently=False)

        logger.info(f"Kết quả SMTP: {sent}")
        return sent

    except Exception:
        logger.exception("Lỗi khi gửi email qua API")
        raise