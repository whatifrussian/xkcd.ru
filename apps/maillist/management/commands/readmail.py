import sys
import email, email.header, email.utils
import re
import datetime
import hashlib
import logging
import traceback
import os.path
import glob
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils.html import strip_tags, strip_entities

from maillist.models import Mail
from comics.models import Comics


logging.basicConfig(filename=settings.MAILLIST_DIR+'/error.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG)

def import_mail(f):
    message = email.message_from_file(f)
    if message and message['to'].find(settings.MAILLIST_NAME) != -1:
        subject, encoding = email.header.decode_header(message['subject'])[0]
        if encoding:
            subject = subject.decode(encoding)
        match = settings.MAILLIST_HEADER.search(subject)
        if match:
            message_hash = hashlib.sha1(message.as_string())
            if settings.MAILLIST_DIR:
                tfn = "%s/%s.msg" % (settings.MAILLIST_DIR,
                                     message_hash.hexdigest())
                if not os.path.exists(tfn):
                    tf = open(tfn, 'w')
                    tf.write(message.as_string())
                    tf.close()
            comics = match.group(1)
            name, address = email.utils.getaddresses([message['from']])[0]
            name, encoding  = email.header.decode_header(name)[0]
            if not encoding is None:
                name = name.decode(encoding)
            date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(
                    email.utils.parsedate_tz(message['date'])))
            logging.debug('Comics: %s(%s).' % (comics, 
                                                message_hash.hexdigest()))
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == 'text/plain':
                        text = part.get_payload(decode=True).\
                            decode(part.get_content_charset('utf-8'))
                        break
                else:
                    logging.debug('No text/plain in multipart message.')
                    for part in message.walk():
                        if part.get_content_type() == 'text/html':
                            text = part.get_payload(decode=True).\
                                decode(part.get_content_charset('utf-8'))
                            text = strip_entities(strip_tags(text))
                            break
                    else:
                        logging.warning('No text/html in message %s.' %
                                            message_hash.hexdigest())
            else:
                text = message.get_payload(decode=True).\
                    decode(message.get_content_charset('utf-8'))
                if message.get_content_type() == 'text/html':
                    logging.debug('No text/plain in message.')
                    text = strip_entities(strip_tags(text))
            try:
                text = text.split(settings.MAILLIST_FOOTER)[0]
            except:
                pass
            try:
                m = Mail(sender="%s <%s>" % (name, address), message=text,
                         date=date, comics=Comics.objects.get(cid=comics))
                m.save()
            except Comics.DoesNotExist:
                pass


class Command(NoArgsCommand):
    help = "Import incoming mail (from stdin) to database."
    option_list = NoArgsCommand.option_list + (
        make_option('--allmsg', action='store_true', dest='all',
                    default=False,
                    help='Import all .msg files from directory.'),
    )

    def handle_noargs(self, **options):
        try:
            if options.get('all'):
                for fn in glob.glob('*.msg'):
                    import_mail(open(fn))
            else:
                import_mail(sys.stdin)
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            logging.error(
                "".join(traceback.format_exception(exceptionType,
                                                   exceptionValue,
                                                   exceptionTraceback)))
