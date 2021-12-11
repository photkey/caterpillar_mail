import re
import json
import logging
import poplib
import smtplib
import mimetypes
from email import encoders
from pathlib import Path
from email.parser import Parser
from email.header import Header
from email.utils import parseaddr
from caterpillar_log import Log
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import decode_header
from email.mime.multipart import MIMEMultipart


Log("caterpillar_mail")
CURRENT_DIR = Path(__file__).resolve().parent
log=logging.getLogger("caterpillar_mail")


class SendEmail(object):
    def __init__(self, send_mail_server, is_ssl=False):
        if is_ssl:
            self.__smtp = smtplib.SMTP_SSL(send_mail_server)
        else:
            self.__smtp = smtplib.SMTP(send_mail_server)
        self.__is_ssl = is_ssl
        self.__From = ""
        self.__To = []
        self.__password = ""
        self.__subject = ""
        self.__context = ""
        self.__main_msg = None
        self.__attach=[]

    def __del__(self):
        try:
            self.__smtp.quit()
        except:
            pass

    @property
    def From(self):
        return self.__From

    @From.setter
    def From(self, From):
        self.__From = From

    @property
    def To(self):
        return self.__To

    @To.setter
    def To(self, To):
        self.__To = [elem.strip() for elem in To.split(",")]

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pwd):
        self.__password = pwd

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, ctx):
        self.__context = ctx

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject

    @property
    def attach(self):
        return self.__attach

    @attach.setter
    def attach(self,attach):
        if attach.strip():
            for elem in attach.split(","):
                elem=elem.strip()
                if not Path(elem).exists():
                    log.warning(f"当前邮件的附件路径 {attach}，不存在，请检查确认......")
                else:
                    self.__attach.append(elem)

    def __generate_attach_file_data(self,attach):
        data = open(attach, 'rb')
        ctype, encoding = mimetypes.guess_type(attach)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        attach_data = MIMEBase(maintype, subtype)
        attach_data.set_payload(data.read())
        data.close()
        encoders.encode_base64(attach_data)
        # 修改附件名称
        attach_data.add_header('Content-Disposition', 'attachment', filename=Path(attach).name)
        return attach_data


    def send(self):
        self.__main_msg = MIMEMultipart()
        self.__main_msg["From"] = self.__From
        self.__main_msg["To"] = ", ".join(self.__To)
        self.__main_msg["Subject"] = Header(self.__subject, "utf-8")
        self.__main_msg.attach(MIMEText(self.__context))
        if self.__attach:
            for each_attach in self.__attach:
                self.__main_msg.attach(self.__generate_attach_file_data(each_attach))
        self.__smtp.login(self.__From, self.__password)
        self.__smtp.sendmail(self.__From, self.__To, self.__main_msg.as_string())


class Mail(object):
    def __init__(self):
        self.__subject = ""
        self.__from_addr = ""
        self.__from_name = ""
        self.__to_name = []
        self.__to_addr = []
        self.__context = ""
        self.__html = ""
        self.__date = ""

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subj):
        self.__subject = subj

    @property
    def from_addr(self):
        return self.__from_addr

    @from_addr.setter
    def from_addr(self, from_addr):
        self.__from_addr = from_addr

    @property
    def from_name(self):
        return self.__from_name

    @from_name.setter
    def from_name(self, from_name):
        self.__from_name = from_name

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, ctx):
        self.__context = ctx

    @property
    def to_name(self):
        return self.__to_name

    @to_name.setter
    def to_name(self, to_name):
        self.__to_name = to_name

    @property
    def to_addr(self):
        return self.__to_addr

    @to_addr.setter
    def to_addr(self, to_addr):
        self.__to_addr = to_addr

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date


class ReadEmail(object):
    def __init__(self, mail_server, is_ssl=False):
        self.__pop_server = mail_server
        self.__is_ssl = is_ssl
        self.__username = ""
        self.__password = ""
        self.__pop = None

    def get_emails_num(self):
        _, mails, _ = self.__pop.list()
        return len(mails)

    def get_latest_n_email(self, n=1, subject="", from_addr="", to_addr=""):
        _, mails, _ = self.__pop.list()
        index = len(mails)
        results = []
        count = 0
        for i in range(index, 0, -1):
            _, lines, _ = self.__pop.retr(i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg_obj = Parser().parsestr(msg_content)
            obj = Mail()
            email_subject = self.__decode_header_msg(msg_obj["subject"])
            if subject.strip() and subject.strip() != email_subject and not re.search(subject.strip(), email_subject):
                continue
            obj.subject = email_subject
            email_from_name, email_from_addr = parseaddr(msg_obj["From"])
            email_from_name = self.__decode_header_msg(email_from_name)
            email_from_addr = self.__decode_header_msg(email_from_addr)
            if from_addr.strip() and from_addr.strip() not in email_from_addr and not re.search(from_addr,
                                                                                                email_from_addr):
                continue
            obj.from_name = email_from_name
            obj.from_addr = email_from_addr

            email_to_name = []
            email_to_addr = []
            for elem in msg_obj["To"].split(","):
                temp_email_to_name, temp_email_to_addr = parseaddr(elem)
                temp_email_to_name = self.__decode_header_msg(temp_email_to_name)
                temp_email_to_addr = self.__decode_header_msg(temp_email_to_addr)
                email_to_name.append(temp_email_to_name)
                email_to_addr.append(temp_email_to_addr)

            to_addr = to_addr.strip()
            to_addr_flag = False
            if to_addr:
                for addr in email_to_addr:
                    if to_addr in addr or re.search(to_addr, addr):
                        to_addr_flag = True
                        break
                if not to_addr_flag:
                    continue

            obj.to_name = email_to_name
            obj.to_addr = email_to_addr
            email_date = self.__decode_header_msg(msg_obj["Date"])
            obj.date = email_date

            context = []
            if msg_obj.is_multipart():
                for part in msg_obj.get_payload():
                    ctx = self.__decode_body(part)
                    if ctx:
                        context.append(ctx)
            else:
                ctx = self.__decode_body(msg_obj)
                if ctx:
                    context.append(ctx)
            if context:
                obj.context = "\n".join(context)

            count += 1
            results.append(obj)
            if count >= n:
                return results

        return results

    def login(self, username, password):
        self.__username = username
        self.__password = password
        if self.__is_ssl:
            self.__pop = poplib.POP3_SSL(self.__pop_server)
        else:
            self.__pop = poplib.POP3(self.__pop_server)

        self.__pop.set_debuglevel(1)
        self.__pop.user(username)
        self.__pop.pass_(password)


    def __decode_header_msg(self, header):
        value, charset = decode_header(header)[0]
        if charset:
            value = value.decode(charset)
        return value

    def __decode_body(self, part):
        content_type = part.get_content_type()
        txt = ""
        if content_type == "text/plain" or content_type == 'text/html':
            content = part.get_payload(decode=True)
            charset = part.get_charset()
            if charset is None:
                content_type_get = part.get('Content-Type', '').lower()
                position = content_type_get.find('charset=')
                if position >= 0:
                    charset = content_type_get[position + 8:].strip()
                    if charset:
                        txt = content.decode(charset)
        return txt


class Email(object):
    def __init__(self, username, auth_code):
        self.__username = username
        self.__auth_code = auth_code
        self.__send_email = None
        self.__read_email = None
        with open(CURRENT_DIR / "email_suffix_to_server.json") as f:
            self.__suffix_to_server = json.load(f)

    def __init_send_email(self):
        suffix = self.__username.split("@")[-1].strip()
        if suffix in self.__suffix_to_server.keys():
            self.__send_email = SendEmail(self.__suffix_to_server[suffix]["smtp"],
                                          is_ssl=self.__suffix_to_server[suffix]["ssl"])
        else:
            raise ValueError(
                f"暂不支持{suffix}类型的邮箱，请到到https://gitee.com/redrose2100/caterpillar_mail或者https://github.com/redrose2100/caterpillar_mail 提Issue需求，目前支持的邮箱如下：{'  '.join(list(self.__suffix_to_server.keys()))}")

    def __init_read_email(self):
        suffix = self.__username.split("@")[-1].strip()
        if suffix in self.__suffix_to_server.keys():
            self.__read_email = ReadEmail(self.__suffix_to_server[suffix]["pop"],
                                          is_ssl=self.__suffix_to_server[suffix]["ssl"])
        else:
            raise ValueError(
                f"暂不支持{suffix}类型的邮箱，请到到https://gitee.com/redrose2100/caterpillar_mail或者https://github.com/redrose2100/caterpillar_mail 提Issue需求，目前支持的邮箱如下：{'  '.join(list(self.__suffix_to_server.keys()))}")

    def send(self, to_addrs, subject="", context="",attach=""):
        """
        功能：发送邮件
        :param to_addr: 收件人邮箱地址
        :param subject: 邮件标题
        :param context: 邮件内容
        :return:
        """
        if not self.__send_email:
            self.__init_send_email()
        self.__send_email.password = self.__auth_code
        self.__send_email.From = self.__username
        self.__send_email.To = to_addrs
        self.__send_email.context = context
        self.__send_email.subject = subject
        self.__send_email.attach = attach
        self.__send_email.send()

    def get_all_emails_num(self):
        if not self.__read_email:
            self.__init_read_email()
        self.__read_email.login(self.__username, self.__auth_code)
        return self.__read_email.get_emails_num()

    def get_latest_n_email(self, n=1, subject="", from_addr="", to_addr=""):
        if not self.__read_email:
            self.__init_read_email()
        self.__read_email.login(self.__username, self.__auth_code)
        return self.__read_email.get_latest_n_email(n=n, subject=subject, from_addr=from_addr, to_addr=to_addr)

    def get_latest_email(self, subject="", from_addr="", to_addr=""):
        """
        功能：返回最新的邮件
        @param subject: 邮件主题过滤条件，可选，不填时默认不进行过滤，支持子串或者正则匹配
        @param from_addr: 发件人邮箱
        @param to_addr: 收件人邮箱
        @return:
        """
        if not self.__read_email:
            self.__init_read_email()
        self.__read_email.login(self.__username, self.__auth_code)
        objs = self.__read_email.get_latest_n_email(n=1, subject=subject, from_addr=from_addr, to_addr=to_addr)
        if objs:
            return objs[0]
