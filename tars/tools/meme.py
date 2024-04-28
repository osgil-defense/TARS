import math
import tiktoken

def tokens_counter(model_name: str, string: str) -> int:
    encoding_name = tiktoken.encoding_for_model(model_name)
    encoding = tiktoken.get_encoding(encoding_name.name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def trim_end(text, model_name, max_size, p, rs=10):
    new_text = str(text)
    current_token_size = tokens_counter(model_name, text)

    while current_token_size > max_size and len(new_text) >= rs:
        tokens = new_text.split()
        rs = min(rs, math.ceil(len(tokens) / 2))
        last_token = tokens[-rs]
        new_text = new_text[:-(len(last_token) + 1)]  # +1 to remove the space before last_token
        current_token_size = tokens_counter(model_name, new_text)
        rs = int(abs(max_size - current_token_size) * p)
        rs = max(1, rs)
        
        # print("{}() - [ Current Token Size: {} | Text Length: {} | RS Value: {} ]".format(trim_end.__name__, current_token_size, len(new_text), rs))
    
    percentage = len(new_text) / len(text)

    return new_text, percentage

text = "Atoms are the basic particles of the chemical elements. An atom consists of a nucleus of protons and generally neutrons, surrounded by an electromagnetically bound swarm of electrons. The chemical elements are distinguished from each other by the number of protons that are in their atoms. For example, any atom that contains 11 protons is sodium, and any atom that contains 29 protons is copper. Atoms with the same number of protons but a different number of neutrons are called isotopes of the same element. Atoms are extremely small, typically around 100 picometers across. A human hair is about a million carbon atoms wide. This is smaller than the shortest wavelength of visible light, which means humans cannot see atoms with conventional microscopes. Atoms are so small that accurately predicting their behavior using classical physics is not possible due to quantum effects. More than 99.94% of an atom's mass is in the nucleus. Protons have a positive electric charge and neutrons have no charge, so the nucleus is positively charged. The electrons are negatively charged, and this opposing charge is what binds them to the nucleus. If the numbers of protons and electrons are equal, as they normally are, then the atom is electrically neutral as a whole. If an atom has more electrons than protons, then it has an overall negative charge, and is called a negative ion (or anion). Conversely, if it has more protons than electrons, it has a positive charge, and is called a positive ion (or cation). The electrons of an atom are attracted to the protons in an atomic nucleus by the electromagnetic force. The protons and neutrons in the nucleus are attracted to each other by the nuclear force. This force is usually stronger than the electromagnetic force that repels the positively charged protons from one another. Under certain circumstances, the repelling electromagnetic force becomes stronger than the nuclear force. In this case, the nucleus splits and leaves behind different elements. This is a form of nuclear decay. Atoms can attach to one or more other atoms by chemical bonds to form chemical compounds such as molecules or crystals. The ability of atoms to attach and detach from each other is responsible for most of the physical changes observed in nature. Chemistry is the science that studies these changes."
x = trim_end(text, "gpt-4-turbo-2024-04-09", 10, 0.5)
print(x)
