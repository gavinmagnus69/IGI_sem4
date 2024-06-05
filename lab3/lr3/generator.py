import check_convertion as check

import random

def generate_yield(len: int):
    '''
       Generate list with yield and input numbers.
               :parameter:
                       len(int): len of list
               :return
                     (list): result list
    '''
    for i in range(len):
        yield check.valid_input_int(f"Input numero: ")
  


def generate_list(len: int):
    '''
      Generate list with loop and input numbers.
              :parameter:
                      len(int): len of list
              :return
                    (list): result list
    '''
    gen_list = []
    for i in range(len):
        gen_list.append(check.valid_input_int(f"input numero: "))
    return gen_list    


def generate_random(len: int):
    '''
                  Random Generate list.
                          :parameter:
                                  len(int): len of list
                          :return
                                (list): result list
    '''
    gen_list = []
    for i in range(len):
        gen_list.append(random.randint(-1000, 1000))
    return gen_list    