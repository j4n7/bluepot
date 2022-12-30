from bs4 import BeautifulSoup

import data.offsets as offsets


class Chat:
    offset = offsets.chat
    times_open_offset = offsets.chat_times_open
    messages_sent_count_offset = offsets.chat_messages_sent_count
    message_sent_0_offset = offsets.chat_message_sent_0
    message_sent_0_len_offset = offsets.chat_message_sent_0_len
    message_current_offset = offsets.chat_message_current
    message_current_len_offset = offsets.chat_message_current_len

    def __init__(self, pm):
        self.pm = pm
        self.address = pm.read_int(pm.base_address + Chat.offset)

    @property
    def times_open(self):
        address = self.address + Chat.times_open_offset
        times_open = self.pm.read_int(address)
        return times_open

    @property
    def is_open(self):
        return bool(self.times_open)

    @property
    def messages_sent_count(self):
        address = self.address + Chat.messages_sent_count_offset
        messages_sent_count = self.pm.read_int(address)
        return messages_sent_count

    @property
    def messages_sent(self):
        address_message_sent_0_len = self.address + Chat.message_sent_0_len_offset
        pointer_message_sent_0 = self.address + Chat.message_sent_0_offset

        for n in range(self.messages_sent_count):
            address_message_sent_n_len = address_message_sent_0_len + n * 0xC

            pointer_message_sent_n = pointer_message_sent_0 + n * 0xC
            address_message_sent_n = self.pm.read_int(pointer_message_sent_n)

            message_sent_n_len = self.pm.read_int(address_message_sent_n_len)
            message_sent_n = self.pm.read_string(address_message_sent_n, byte=message_sent_n_len)
            soup = BeautifulSoup(message_sent_n, features="lxml")
            yield soup.text

    @property
    def message_current(self):
        '''
        Text16Ptr points to an address
        In that address you find the first letter string
        You need to sum 0x2 to get all letters (1 letter each 2 bytes)
        Stop when you reach message length
        '''
        address_message_current_len = self.address + Chat.message_current_len_offset

        pointer_message_current = self.address + Chat.message_current_offset
        address_message_current = self.pm.read_int(pointer_message_current)

        message_current_len = self.pm.read_int(address_message_current_len)
        message_current = ''.join([self.pm.read_string(address_message_current + n * 0x2) for n in range(message_current_len)])

        return message_current
