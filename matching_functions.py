import glob, re, codecs, re, time, math, string, pickle
from lxml import etree
#from nltk.corpus import stopwords

#sw = set(stopwords.words('english') + ['thee', 'thy', 'thou', 'thine'] + ['a','ab','ac','ad','at','atque','aut','autem','cum','de','dum','e','erant','erat','est','et','etiam','ex','haec','hic','hoc','in','ita','me','nec','neque','non','per','qua','quae','quam','qui','quibus','quidem','quo','quod','re','rebus','rem','res','sed','si','sic','sunt','tamen','tandem','te','ut','vel'])

# Same as above, except that I removed "no", "nor", "not", "non".

sw = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'thee', 'thy', 'thou', 'thine', 'a', 'ab', 'ac', 'ad', 'at', 'atque', 'aut', 'autem', 'cum', 'de', 'dum', 'e', 'erant', 'erat', 'est', 'et', 'etiam', 'ex', 'haec', 'hic', 'hoc', 'in', 'ita', 'me', 'nec', 'neque', 'per', 'qua', 'quae', 'quam', 'qui', 'quibus', 'quidem', 'quo', 'quod', 're', 'rebus', 'rem', 'res', 'sed', 'si', 'sic', 'sunt', 'tamen', 'tandem', 'te', 'ut', 'vel'])

bogus_characters = set('!"&\'()*+,-.0123456789?\\^_`{|¯°´·¼½¾×÷þƿȝȳʋʒ˘̔άαβγδεζηθικλμνξοπρςστυφχψωόύϛϲ֖֥֧֔֙֨אבגדהוזחטיכלםמןנסעפצקרשת؛ḍḡḷṅụỽỿ‘•…′″‴℈ℛ℞℟℣℥⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞ↁↂↄↇↈ−√∝∞∠∣∥∧∨∩∴∵∶∷∼∽⊕⊗⊙⊢⊣⊦⊽⋆⋮⌊①②③④⑤⑥⑦⑨⓪╌■□▪▭△▵▿◆◊○●★☉☊☋☌☍☐☜☝☞☟☧☼☽☾☿♀♁♂♃♄♈♉♊♋♌♍♎♏♐♑♒♓♠♡♣♫♭♮♯⚀⚁⚂⚃⚄⚅⚜⚹✚✝✦✴✿❀❍❧⸪⸫〈〉ꝑꝓꝗꝙꝧꝫꝭꝯꝰ텥텮텯톹톺톼ﬂﬄ𝄞𝄡𝄢𝆶𝆷𝆸𝆹𝇁𝇂𝇆𝇇𝇈𝇊𝇋𝇌𝇍𝇎💀🜁🜂🜃🜄🜅🜆🜊🜋🜍🜓🜔🜕🜖🜘🜭🜹🜺🜽🜿🝁🝆🝊🝕🝗🝘🝞🝟🝣🝪🝯1​')


def load_metadata(METADATA_FILE_NAME):

    metadata = {}

    for line in codecs.open(METADATA_FILE_NAME, 'r', encoding='utf-8').read().split('\n'):
        if line.strip() > '' and len(line.strip().split('\t')) > 3:
            cols = line.strip().split('\t')
            metadata[cols[0]] = {'year': cols[1], 'author': cols[2], 'title': cols[3]}

    return metadata

def is_lemma_valid(lemma):
    
    result = True
    
    if lemma == None:
        result = False
    elif len(bogus_characters.intersection(lemma)) > 0:
        result = False
    
    return result

def select_token_and_lemma(node, token_attribute):
    
    selected_token = None
    selected_lemma = None
    
    if node.tag.endswith('}c'):
        selected_token = ' '
        selected_lemma = ' '

    elif node.tag.endswith('}pc'):

        if node.get(token_attribute) != None:
            selected_token = node.get(token_attribute)
        else:
            selected_token = ' '

        selected_lemma = ' '

    elif node.tag.endswith('}w'):

        if node.get(token_attribute) != None:
            selected_token = node.get(token_attribute)
        else:
            selected_token = ' '

        if node.get('lem') != None:
            if node.get('lem').lower() in sw or is_lemma_valid(node.get('lem').lower()) == False:
                selected_lemma = ' '
            else:
                selected_lemma = node.get('lem').lower()
        else:
            selected_lemma = ' '
            
    return selected_token, selected_lemma

def get_tokens_for_iterator(node, token_attribute='spe'):

    tokens = []
    lemmas = []
    
    for token in node.iter():
        selected_token, selected_lemma = select_token_and_lemma(token, token_attribute)
        if selected_token != None and selected_lemma != None:
            tokens.append(selected_token)
            lemmas.append(selected_lemma)
        
    return tokens, lemmas
    
def tokenize_lemmatize_one_file(path_to_file, token_attribute='spe'):

    tree = etree.parse(path_to_file)
    
    tokens, lemmas = get_tokens_for_iterator(tree, token_attribute)

    return tokens, lemmas

def get_non_space_lemmas_and_offsets(lemmas):
    
    non_space_lemmas = []
    offsets = []
    
    for offset, lemma in enumerate(lemmas):
        if lemma.strip() > '':
            non_space_lemmas.append(lemma)
            offsets.append(offset)
            
    return non_space_lemmas, offsets

def shingle_tokens(non_space_lemma, SHINGLE_LENGTH):
    
    shingles = {}
    
    for a in range(0, len(non_space_lemma) - SHINGLE_LENGTH + 1):
        try:
            shingles[tuple(non_space_lemma[a: a + SHINGLE_LENGTH])].append([a, a + SHINGLE_LENGTH - 1])
        except KeyError:
            shingles[tuple(non_space_lemma[a: a + SHINGLE_LENGTH])] = [[a, a + SHINGLE_LENGTH - 1]]
                
    return shingles

def preprocess_one_file(path_to_file, SHINGLE_LENGTH, token_attribute='spe'):
    
    tokens, lemmas = tokenize_lemmatize_one_file(path_to_file)
    non_space_lemmas, offsets = get_non_space_lemmas_and_offsets(lemmas)
    shingles = shingle_tokens(non_space_lemmas, SHINGLE_LENGTH)
    
    return {'tokens': tokens, 'lemmas': lemmas,
            'non_space_lemmas': non_space_lemmas, 'offsets': offsets,
            'shingles': shingles}

def load_pickle_file(p):
    
    f = open(p, 'rb')
    data = pickle.load(f)
    f.close()
    
    return data

def match_two_files(file_a, file_b, 
                        MAX_GAP_ALLOWED, MIN_MATCH_LENGTH,
                        return_match_offsets=False):
    
    final_results = []
    
    matches = []
    for k in file_a['shingles'].keys():
        if k in file_b['shingles']:
            for v_a in file_a['shingles'][k]:
                for v_b in file_b['shingles'][k]:
                    matches.append([v_a, v_b])
    
    matches.sort()
    
    if len(matches) > 0:
    
        grouped_matches = [[matches[0],],]

        for m in matches[1:]:

            group_match_n = -1
            for gn, g in enumerate(grouped_matches):
                if (m[0][0] - MAX_GAP_ALLOWED) < g[-1][0][1] and \
                    (m[1][0] - MAX_GAP_ALLOWED) < g[-1][1][1] and \
                    m[0][0] > g[-1][0][0] and \
                    m[1][0] > g[-1][1][0]:

                    group_match_n = gn
                    break

            if group_match_n > -1:
                grouped_matches[gn].append(m)
            else:
                grouped_matches.append([m])

        merged_matches = []
        for gn, g in enumerate(grouped_matches):

            from_matches = []
            to_matches = []
            for m in g:
                from_matches.append(m[0])
                to_matches.append(m[1])

            from_matches.sort()
            to_matches.sort()

            if from_matches[-1][1] - from_matches[0][0] >= MIN_MATCH_LENGTH - 1: 

                merged_matches.append([[from_matches[0][0], from_matches[-1][1]], 
                                        [to_matches[0][0], to_matches[-1][1]]])

        for mn, m in enumerate(merged_matches):

            a_from_offset = file_a['offsets'][m[0][0]]
            a_to_offset = file_a['offsets'][m[0][1]]

            b_from_offset = file_b['offsets'][m[1][0]]
            b_to_offset = file_b['offsets'][m[1][1]]
            
            if return_match_offsets == True:
                final_results.append([''.join(file_a['tokens'][a_from_offset: a_to_offset + 1]),
                                        ''.join(file_b['tokens'][b_from_offset: b_to_offset + 1]),
                                        [a_from_offset, a_to_offset], [b_from_offset, b_to_offset]])
            else:
                final_results.append([''.join(file_a['tokens'][a_from_offset: a_to_offset + 1]),
                                        ''.join(file_b['tokens'][b_from_offset: b_to_offset + 1])])

    return final_results
