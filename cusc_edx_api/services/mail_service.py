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
):
    """
    Gửi email HTML + plain text từ template Django.

    Args:
        to_emails (str | list[str]): Email người nhận (chuỗi hoặc danh sách)
        subject (str): Tiêu đề email
        template_name (str): Tên file template (ví dụ: 'emails/welcome.html')
        context (dict): Dữ liệu truyền vào template

    Returns:
        int: Số lượng email đã gửi thành công (thường là 1)

    Raises:
        ValueError: Nếu thiếu email người nhận hoặc template render rỗng
    """
    # Chuẩn hóa danh sách email người nhận
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    if not to_emails or not all(to_emails):
        logger.error("Không có email người nhận hợp lệ")
        raise ValueError("Missing valid recipient email(s)")


    try:
    
        html_content = render_to_string(template_name, context)

        if not html_content or not html_content.strip():
            raise ValueError(f"Template '{template_name}' render ra nội dung rỗng")

       
        text_content = strip_tags(html_content)

        logger.info(f"Gửi email từ → {to_emails} | Subject: {subject}")

    
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            to=to_emails,
        )

    
        msg.attach_alternative(html_content, "text/html")

     
        sent_count = msg.send(fail_silently=False)

        logger.info(f"Gửi email thành công - SMTP trả về: {sent_count}")
        return sent_count

    except Exception:
        logger.exception(
            f"Lỗi khi gửi email | to: {to_emails} | subject: {subject}"
        )
        raise