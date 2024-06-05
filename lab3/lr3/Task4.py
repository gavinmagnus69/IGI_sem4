
import prints

input_text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."


def get_words(txt : str) -> list:
    '''
       Split string in list of words  and erase , and . in words.
       :parameter
            txt(str): input string
        :return
            words(list):  result words
    '''
    words = txt.split()
    for i in range(len(words)):
        if words[i][-1] == '.' or words[i][-1] == ',':
            words[i] = words[i][:-1]
    return words


def get_len(words: list) -> int:
    '''
       this function returns an integer length of list
    '''

    return len(words)

def get_even(words: list) -> int:
    '''
       this function returns list of words with even number of letters in your given list of words
    '''


    even_words = list()
    for i in words:
        if len(i) % 2 == 0:
            even_words.append(i)
    return even_words


def get_shortest_a(words: list) -> str:
    '''
       this function returns a shortest string starting with 'a' in your given list of words
    '''
    shortest = 'bbbbbbbbbbbbbbbbbbbbb'
    for word in words:
        if word[0] == 'a':
            if len(word) <= len(shortest):
                 shortest = word
    return shortest

def get_repeated(words: list) -> str:
    '''
       this function returns a list of repeated words in your given list of words
    '''
    word_dict = {}
    ans = []
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1    
    for word, count in word_dict.items():
        if count > 1:
            ans.append(word)
    return ans


def main():
    while True:
        words = get_words(input_text)

        if not len(words):
            print("your string is empty")
        else:
            print("\ndetermine the number of words in a line and display all words with an even number of letters")
            print(f"the number of words: {get_len(words)}")
            print("words with even number of letters:")
            print(get_even(words))
            print(f"\nfind the shortest word that starts with 'a': {get_shortest_a(words)}")
            print("\ndisplay duplicate words: ")
            print(get_repeated(words))
        if not prints.try_again():
            break


        
if __name__ == "__main__":
    main()                

