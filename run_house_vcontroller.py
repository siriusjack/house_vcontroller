from juliuspy import Julius
from camphor_house import House
import re
import json
from logging import getLogger,StreamHandler,DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class KeywordLister():
    def __init__(self):
        self.__julius = Julius(host='localhost', port=10500)
        self.__julius.connect()

    def __del__(self):
        self.__julius.disconenct()

    @staticmethod
    def filter_recognout(stream):
        reg = re.compile(r'WHYPO WORD="(.*)" CLASSID="(.*)" PHONE="(.*)" CM="(\d\.\d{3})"')
        for msg in stream:
            match = re.search(reg, msg)
            if match:
                word, cid, phone, cm = match.groups(1)
                yield json.dumps({'word': word, 'cid': cid, 'phone':phone, 'cm': cm}, ensure_ascii=False)

    @staticmethod
    def filter_by_cm(stream, threshold):
        for msg in stream:
            j = json.loads(msg)
            if float(j['cm']) > threshold:
                yield msg

    def listen(self, cm_threshold):
        stream = self.__julius.get_stream()
        recognout = self.filter_recognout(stream)
        return self.filter_by_cm(recognout, cm_threshold)


def main():
    house = House()
    k_listener = KeywordLister()

    try:
        for k_msg in k_listener.listen(cm_threshold=0.5):
            logger.debug(k_msg)
            j = json.loads(k_msg)
            house.listen(j['word'])

    except KeyboardInterrupt:
        logger.debug('---- KeyboardInterrupt ---- ')

    except Exception as e:
        logger.error(e.message)


if __name__ == '__main__':
    main()
