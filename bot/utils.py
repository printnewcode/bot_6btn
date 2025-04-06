from datetime import datetime
from pytz import tzinfo

from bot.models import User
from Control.settings import TZ

def is_active(user):
    access_time = user.access_time_end
    if datetime.now().replace(tzinfo=None) < access_time.replace(tzinfo=None):
        return True
    else:
        return False
    
def get_user(id):
    user = User.objects.filter(telegram_id=id).first()
    return user