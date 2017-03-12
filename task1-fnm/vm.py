import numpy as np

WORD_SIZE = 4
INSTRUCTION_SIZE = 12

def convert_word_to_bytes(int32_val):
    bin = np.binary_repr(int32_val, width = 32) 
    int8_arr = [int(bin[0:8],2), int(bin[8:16],2), 
                int(bin[16:24],2), int(bin[24:32],2)]
    return int8_arr

def convert_bytes_to_word(bts):
    str_bts = list(map( lambda bt: np.binary_repr(bt, width = 8), bts))
    return int(''.join(str_bts), 2)

class Memory:
    __init__(self, memory_size):
        self.memory = np.zeros( memory_size, dtype=np.int8 )
    
    def write_word(self, adress, word: np.int ):
        bts = convert_word_to_bytes(word)
        for i in range(len(bts)):
            self.memory[adress + i] = bts[i]

    def read_word(self, adress):
        bytes_word = self.memory[adress : adress + WORD_SIZE]
        return convert_bytes_to_word(bytes_word)

ARG_ACCESS_IMMEDIATE = 0
ARG_ACCESS_DIRECT = 1
ARG_ACCESS_INDIRECT = 2

COMMAND_MOV = 0
COMMAND_ADD = 1
COMMAND_SUB = 2
COMMAND_POP = 3
COMMAND_PUSH = 4
COMMAND_CALL = 5
COMMAND_FUNCB = 6
COMMAND_FUNCE = 7
COMMAND_TERMINATE = 8

IP_INDEX = 0
SP_INDEX = 1

class Interpreter:

    __init__(self, memory):
        self.memory = memory
        self.function_startpoints = {}
        self.reading_function = False

    def ip_value(self):
        return self.memory.read_word(IP_INDEX)

    def ip_address(self):
        return IP_INDEX

    def sp_value(self):
        return self.memory.read_word(SP_INDEX)

    def sp_address(self):
        return SP_INDEX

    def get_value(self, value, access):
        if access == ARG_ACCESS_IMMEDIATE:
            return value
        elif access == ARG_ACCESS_INDIRECT:
            return self.memory.read_word(value)
        elif access == ARG_ACCESS_DIRECT:
            return self.memory.read_word(self.memory.read_word(value))

    def mov(self, dest, src, src_access):
        src_value = self.get_value(self.memory, src, src_access)
        self.memory.write_word(dest, src_value)
        self.next_command()

    def add(self, dest, addition, addition_access):
        addition_value = self.get_value(self.memory, addition, addition_access)
        self.memory.write_word(dest, memory.read_word(dest) + addition_value)
        self.next_command()

    def next_command(self):
        self.add(self.ip_address, INSTRUCTION_SIZE, ARG_ACCESS_IMMEDIATE)

    def sub(self, dest, sub, sub_access):
        sub_value = self.get_value(memory, sub, sub_access)
        self.memory.write_word(dest, self.memory.read_word(dest) - sub_value)
        self.next_command()
    
    def jump(self, dest, dest_access):
        instruction_number = self.get_value(dest, dest_access)
        self.memory.write_word(ip_adress(), instruction_number)

    def jgz(self, val, val_access, dest, dest_access):
        value = self.get_value(val, val_access)
        if value >= 0:
            self.jump(dest, dest_access)
        else:
            self.next_command()

    def pop(self):
        self.add(self.sp_address(), 1, ARG_ACCESS_IMMEDIATE)
        self.next_command()

    def push(self, val, val_access):
        self.sub(self.sp_adress(), 1, ARG_ACCESS_IMMEDIATE)
        self.memory.write_word(self.sp_value(), self.get_value(val, val_access))
        self.next_command()
    
    def call(self, val):
        self.memory.write_word(self.ip_address(), self.function_startpoints[val])
    
    def func_begin(self, number, number_access):
        num = self.get_value(number, number_access)
        self.function_startpoints[num] = self.ip_address() + INSTRUCTION_SIZE
        self.reading_function = True
    
    def func_end(self):
        self.reading_function = False

    def interpret_next_command(self):
        instruction = self.get_value(self.ip_value(), ARG_ACCESS_DIRECT)
        argument1 = self.get_value(self.ip_value() + WORD_SIZE, ARG_ACCESS_DIRECT)
        argument2 = self.get_value(self.ip_value() + 2 * WORD_SIZE, ARG_ACCESS_DIRECT)

        instruction_code = instruction & 0xffff0000 >> 4
        first_arg_access = instruction & 0x0000ff00 >> 2
        second_arg_access = instruction & 0x000000ff

        if instruction_code == COMMAND_MOV:
            self.mov(argument1, argument2, second_arg_access)
        elif instruction_code == COMMAND_ADD:
            self.add(argument1, argument2, second_arg_access)
        elif instruction_code == COMMAND_CALL:
            self.call(argument1)
        elif instruction_code == COMMAND_SUB:
            self.sub(argument1, argument2, second_arg_access)
        elif instruction_code == COMMAND_POP:
            self.pop()
        elif instruction_code == COMMAND_PUSH:
            self.push(argument1, first_arg_access)
        elif instruction_code == COMMAND_FUNCB:
            self.func_begin(argument1, first_arg_access)
        elif instruction_code == COMMAND_FUNCE:
            self.func_end()
        elif instruction_code == COMMAND_TERMINATE:
            return True
        return False

    def run_execution(self):
        while self.interpret_next_command():
            if self.reading_function:
                while self.reading_function:
                    self.next_command()

