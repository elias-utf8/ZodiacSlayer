import numpy as np
import re

# Texte fourni
text_sequence =(
    "IEEBSUUTAOORYEATS"
    "OHHNIUYNTTSFLEOCY"
    "ABUOAANTODIHATSFU"
    "UCUESRVMCIUTOELES"
    "NOLOSWETEEYTHHNFE"
    "LNSBWUERAOHSPSAEG"
    "SRAGYEHNIOTRISHED"
    "EFOEGTMCETTNOTDAE"
    "GRMOLAHHBANBMGOOD"
    "LOOWFUNLOYAHIOOPA"
    "CTOYDHLETLDININUO"
    "CNOUNOIAASCTLUDSA"
    "ILATBLGUSTGSAHENY"
    "DOSFNFCAFWIIAYRIT"
    "SMEUTLUSOTLAOSNOE"
    "UOFERSHASENNANVTD"
    "HIDFLSSOEGERGOGTE"
    "TREGOAOATTFYSDRNS"
)
text_sequence2=(
    "IEEBSUUTAORYEATSO"
    "HHNIUYNTTSFEOCYAB"
    "UAANTODIHATSFUUCU"
    "ESRVMCIUTELESNOLC"
    "TEEYTHHNFENSTUERA"
    "HSPSAEGSRAGYEHNIO"
    "TRISHEDEFEGTMCETT"
    "NOTDAEGRMOLAHHBAN"
    "BMGODLOOWFUNLOYAH"
    "IOOFASTOYDHLETLDI"
    "NINUOCNEUNIAASCTL"
    "UDSAILAIRGUSTGSAH"
    "ENYDOSFNVCAFWCIAY"
    "RITSMEUTLUHTLASNO"
    "EUOFERSHASUNIANVT"
    "DHIDFLSSOEGEGGGTE"
    "TREGOAOATTFYSTRNS"
)

# Liste des indices fournie
original_indices = [
    1, 10, 19, 28, 37, 46, 55, 64, 73, 82, 91, 100, 109, 118, 127, 136, 145,
    137, 146, 2, 11, 20, 29, 38, 47, 56, 65, 74, 83, 92, 101, 110, 119, 128,
    120, 129, 138, 147, 3, 12, 21, 30, 39, 48, 57, 66, 75, 84, 93, 102, 111,
    103, 112, 121, 130, 139, 148, 4, 13, 22, 31, 40, 49, 58, 67, 76, 85, 94,
    86, 95, 104, 113, 122, 131, 140, 149, 5, 14, 23, 32, 41, 50, 59, 68, 77,
    69, 78, 87, 96, 105, 114, 123, 132, 141, 150, 6, 15, 24, 33, 42, 51, 60,
    52, 61, 70, 79, 88, 97, 106, 115, 124, 133, 142, 151, 7, 16, 25, 34, 43,
    35, 44, 53, 62, 71, 80, 89, 98, 107, 116, 125, 134, 143, 152, 8, 17, 26,
    18, 27, 36, 45, 54, 63, 72, 81, 90, 99, 108, 117, 126, 135, 144, 153, 9,
    154, 163, 172, 181, 190, 199, 208, 217, 226, 235, 244, 253, 262, 271, 280, 289, 298,
    290, 299, 155, 164, 173, 182, 191, 200, 209, 218, 227, 236, 245, 254, 263, 272, 281,
    273, 282, 291, 300, 156, 165, 174, 183, 192, 201, 210, 219, 228, 237, 246, 255, 264,
    256, 265, 274, 283, 292, 301, 157, 166, 175, 184, 193, 202, 211, 220, 229, 238, 247,
    239, 248, 257, 266, 275, 284, 293, 302, 158, 167, 176, 185, 194, 203, 212, 221, 230,
    222, 231, 240, 249, 258, 267, 276, 285, 294, 303, 159, 168, 177, 186, 195, 204, 213,
    205, 214, 223, 232, 241, 250, 259, 268, 277, 286, 295, 304, 160, 169, 178, 187, 196,
    188, 197, 206, 215, 224, 233, 242, 251, 260, 269, 278, 287, 296, 305, 161, 170, 179,
    171, 180, 189, 198, 207, 216, 225, 234, 243, 252, 261, 270, 279, 288, 297, 306, 162
]
final=[]
message=""
print(len(text_sequence))
for i in range(len(text_sequence)):
    temp = f"{str(original_indices[i])}"+f"{text_sequence[i]}"
    final.append(temp)
final = sorted(final, key=lambda x: int(''.join(filter(str.isdigit, x))))
final = [re.sub(r'\d+', '', s) for s in final]
for i in range(len(final)):
    message+=(final[i])
print(message)
