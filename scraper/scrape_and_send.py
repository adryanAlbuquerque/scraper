import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT



def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')


        titles = soup.find_all('h1')
        extracted_data = [title.get_text() for title in titles]

        return extracted_data
    except Exception as e:
        print(f"Erro ao fazer scraping: {e}")
        return []


def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))


        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)
        server.quit()

        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def main():
    url = 'https://www.linkedin.com/in/adryan13/' 
    data = scrape_data(url)
    
    if data:
        subject = "Dados Extraídos do Scraping"
        body = '\n'.join(data)
        send_email(subject, body)
    else:
        print("Nenhum dado extraído para enviar.")

if __name__ == "__main__":
    main()
