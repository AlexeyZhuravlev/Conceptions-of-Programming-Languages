import numpy as np

WORD_SIZE = 4
INSTRUCTION_SIZE = 5 * WORD_SIZE
NUMBER_OF_REGISTERS = 8

COMMAND_MOV = 0
COMMAND_ADD = 1
COMMAND_SUB = 2
COMMAND_POP = 3
COMMAND_PUSH = 4
COMMAND_CALL = 5
COMMAND_FUNCB = 6
COMMAND_FUNCE = 7
COMMAND_TERMINATE = 8
COMMAND_JUMP = 9
COMMAND_RJGZ = 10

IP_INDEX = 0
SP_INDEX = 1

class Memory:
    def __init__(self, memory_size):
        self.memory = np.zeros( memory_size, dtype=np.int8 )

    def convert_word_to_bytes(self, int32_val):
        bin = np.binary_repr(int32_val, width=32)
        int8_arr = [int(bin[0:8], 2), int(bin[8:16], 2),
                    int(bin[16:24], 2), int(bin[24:32], 2)]
        return int8_arr

    def convert_bytes_to_word(self, bts):
        str_bts = list(map(lambda bt: np.binary_repr(bt, width=8), bts))
        return int(''.join(str_bts), 2)

    def write_word(self, address, word ):
        bts = self.convert_word_to_bytes(word)
        for i in range(len(bts)):
            self.memory[address + i] = bts[i]

    def read_word(self, adrdess):
        bytes_word = self.memory[address : address + WORD_SIZE]
        return self.convert_bytes_to_word(bytes_word)

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
        for i in range(access):
            value = self.memroy.read_word(value)
        return value

    def mov(self, dest, dest_access, src, src_access):
        dest_address = self.get_value(dest, dest_access)
        src_value = self.get_value(src, src_access)
        self.memory.write_word(dest_address, src_value)
        self.next_command()

    def add(self, dest, dest_access, addition, addition_access):
        dest_address = self.get_value(dest, dest_access)
        addition_value = self.get_value(self.memory, addition, addition_access)
        self.memory.write_word(dest_address, self.memory.read_word(dest) + addition_value)
        self.next_command()

    def next_command(self):
        self.add(self.ip_address(), INSTRUCTION_SIZE, ARG_ACCESS_IMMEDIATE)

    def sub(self, dest, dest_access, sub, sub_access):
        dest_address = self.get_value(dest, dest_access)
        sub_value = self.get_value(self.memory, sub, sub_access)
        self.memory.write_word(dest_address, self.memory.read_word(dest) - sub_value)
        self.next_command()
    
    def jump(self, dest, dest_access):
        instruction_number = self.get_value(dest, dest_access)
        self.memory.write_word(ip_adress(), instruction_number)

    def rjgz(self, val, val_access, dest, dest_access):
        value = self.get_value(val, val_access)
        if value >= 0:
            self.add(IP_INDEX, 0, dest, dest_access)
        else:
            self.next_command()

    def pop(self):
        self.add(self.sp_address(), 0, 1, 0)
        self.next_command()

    def push(self, val, val_access):
        self.sub(self.sp_address(), 0, 1, 0)
        self.memory.write_word(self.sp_value(), self.get_value(val, val_access))
        self.next_command()
    
    def call(self, val, val_access):
        value = self.get_value(val, val_access)
        self.push(self.ip_value(), 0)
        self.memory.write_word(self.ip_address(), self.function_startpoints[value])
    
    def func_begin(self, number, number_access):
        num = self.get_value(number, number_access)
        self.function_startpoints[num] = self.ip_address() + INSTRUCTION_SIZE
        self.reading_function = True
    
    def func_end(self):
        self.reading_function = False

    def interpret_next_command(self):
        instruction = self.get_value(self.ip_value(), 1)
        first_arg_access = self.get_value(self.ip_value() + WORD_SIZE, 1)
        argument1 = self.get_value(self.ip_value() + 2 * WORD_SIZE, 1)
        second_arg_access = self.get_value(self.ip_value() + 3 * WORD_SIZE, 1)
        argument2 = self.get_value(self.ip_value() + 4 * WORD_SIZE, 1)

        if self.reading_function and not instruction == COMMAND_FUNCE:
            return True

        if instruction_code == COMMAND_MOV:
            self.mov(argument1, first_arg_access, argument2, second_arg_access)
        elif instruction_code == COMMAND_ADD:
            self.add(argument1, first_arg_access, argument2, second_arg_access)
        elif instruction_code == COMMAND_CALL:
            self.call(argument1, first_arg_access)
        elif instruction_code == COMMAND_SUB:
            self.sub(argument1, first_arg_access, argument2, second_arg_access)
        elif instruction_code == COMMAND_POP:
            self.pop()
        elif instruction_code == COMMAND_PUSH:
            self.push(argument1, first_arg_access, first_arg_access)
        elif instruction_code == COMMAND_FUNCB:
            self.func_begin(argument1, first_arg_access)
        elif instruction_code == COMMAND_FUNCE:
            self.func_end()
        elif instruction_code == COMMAND_JUMP:
            self.jump(argument1, first_arg_access)
        elif instruction_code == COMMAND_RJGZ:
            self.rjgz(argument1, first_arg_access, argument2, second_arg_access)
        elif instruction_code == COMMAND_TERMINATE:
            return False
        return True

    def run_execution(self):
        while self.interpret_next_command():
            pass

if( len(sys.argv) < 2 )
    print "Specify binary filename"

MEMORY_SIZE = 1000000000
Memory memory(MEMORY_SIZE * WORD_SIZE)
memory.write_word(IP_INDEX, NUMBER_OF_REGISTERS * WORD_SIZE)
memory.write_word(SP_INDEX, MEMORY_SIZE * WORD_SIZE)
code = np.fromfile(sys.argv[1])
for i in len(code):
    memory.write_word(NUMBER_OF_REGISTERS * WORD_SIZE + i, code[i])
Interpreter interpreter(memory)
interpreter.run_execution()
