
punctuation = [
    ' ', '!', '"', '#', '%', '&', "'", '(', ')',
    '*', '+', ',', '-', '.', '/',  ':', ';', '=',
    '>', '?','@', '[', '\\', ']', '_', '{', '}',
    '«', '·', '»', '¾', '×','÷',  '،', '؛', '؟',
    '٪',  '–', '‘', '’', '‚',  '÷','“', '”', '…',
    '﴾', '﴿',
    ]

abc_latin_upper = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
abc_latin_lower = list('abcdefghijklmnopqrstuvwxyz')
abc_latin = abc_latin_upper + abc_latin_lower

latin_with_diacrit = ['à', 'å', 'ç', 'è', 'é', 'ê', 'û', 'İ']

abc_arabic = list('ابتثجحخدذرزسشصضطظعغفقكلمنهوي')
abc_arab_hamza = ['ٱ','ء', 'آ', 'أ', 'ؤ', 'إ', 'ئ', 'ى', 'ة']
# abc_arab_hamza += ['']

diacrit_arab = [
    'َ', 
    'ِ',
    'ُ',
    'ً',
    'ٍ',
    'ٌ',
    'ْ',
    'ّ',
    'ٰ']

arab_vowels_short = [
    'َ', # a (fatha)
    'ِ', # i (kasra)
    'ُ', # u (damma)
]

arab_nunation = [
    'ً', # an
    'ٍ', # in
    'ٌ', # un
]

diacrit_an = 'ً' # an

diacrit_sukun = 'ْ' # sukun
diacrit_shadda = 'ّ' # shadda
diacrit_dagger_alif = 'ٰ' # dagger alif

diacrit_arab = [
    'َ', # a (fatha)
    'ِ', # i (kasra)
    'ُ', # u (damma)
    'ً', # an
    'ٍ', # in
    'ٌ', # un
    'ْ', # sukun
    'ّ', # shadda
    'ٰ', # dagger alif
]

abc_arab_extra = ['گ']
arab_special = ['ۖ', 'ۚ', 'ـ']

arab_replace = [
    ('ﺌ','ئ'), # Arabic letter Yeh with Hamza above medial form (65164)
    ('ﺎ','ا'), # Arabic letter Alef final form (65166)
    ('ﺕ','ت'), # Arabic letter Teh isolated form (65173)
    ('ﺠ','ج'), # Arabic letter Jeem medial form (65184)
    ('ﺯ','ز'), # Arabic letter Zain isolated form (65199)
    ('ﻌ','ع'), # Arabic letter Ain medial form (65228)
    ('ﻑ','ف'),  # Arabic letter Feh isolated form (65233)
    ('ﻔ','ف'), # Arabic letter Feh medial form (65236)
    ('ﻴ','ي'), # Arabic letter Yeh medial form (65268)
    (chr(65159), chr(1573)), # Arabic letter Alef with Hamza below isolated form (65159)
    ]
arab_replace = {f:t for (f, t) in arab_replace}

numerals = list('0123456789')
numerals_ar =  list('٠١٢٣٤٥٦٧٨٩')


letters_rm = punctuation + arab_special
letters_unk = abc_latin + abc_arab_extra

letters_ds_unvoc = [' '] + abc_arabic + abc_arab_hamza #+ diacrit_arab #+ numerals + numerals_ar
letters_ds_voc = [' '] + abc_arabic + abc_arab_hamza + diacrit_arab #+ numerals + numerals_ar
