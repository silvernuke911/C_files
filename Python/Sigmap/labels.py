from typing import List, Dict
STREET_LABELS = [
    {
        "name": "University Avenue",
        "x": 121.0685,
        "y": 14.6540,
        "rotation": 0,
        "fontsize": 10,
        "color": "black"
    },
    {
        "name": "C.P. Garcia Avenue",
        "x": 121.0670,
        "y": 14.6535,
        "rotation": 90,
        "fontsize": 9,
        "color": "black"
    },
    # Add more labels as needed...
]

BUILDING_LABELS = [
    {
        "name": "CHR",
        "x": 121.06016,
        "y": 14.65722,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "SP",
        "x": 121.072050,
        "y": 14.659199,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Gonzales Hall",
        "x": 121.07124,
        "y": 14.655109,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CSWCD",
        "x": 121.06361,
        "y": 14.65695,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "SOLAIR",
        "x": 121.06154,
        "y": 14.65710,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NCPAG",
        "x": 121.06056,
        "y": 14.65642,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "ISSI",
        "x": 121.06174,
        "y": 14.65654,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "GPPB",
        "x": 121.06926,
        "y": 14.65698,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CHK",
        "x": 121.06281,
        "y": 14.65934,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UPVan",
        "x": 121.06417,
        "y": 14.65888,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "DMST",
        "x": 121.06423,
        "y": 14.65824,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "SURP",
        "x": 121.06285,
        "y": 14.65726,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CMC",
        "x": 121.06453,
        "y": 14.65670,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CMs",
        "x": 121.06539,
        "y": 14.65666,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Theatre",
        "x": 121.06609,
        "y": 14.65678,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Fonacier",
        "x": 121.065825,
        "y": 14.657821,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UPTC",
        "x": 121.07537,
        "y": 14.65083,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UPFI",
        "x": 121.06702,
        "y": 14.65684,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IBG-KAL",
        "x": 121.06816,
        "y": 14.65719,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Melchor Hall",
        "x": 121.069511,
        "y": 14.656550,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Carillion",
        "x": 121.066575,
        "y": 14.656331,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NEC",
        "x": 121.07118,
        "y": 14.65661,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "GYH",
        "x": 121.07118,
        "y": 14.65721,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Malcolm",
        "x": 121.07210,
        "y": 14.65674,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "BahayNgAlumni",
        "x": 121.06665,
        "y": 14.65805,
        "rotation": 90,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Molave",
        "x": 121.06766,
        "y": 14.65794,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Yakal",
        "x": 121.06904,
        "y": 14.65811,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Ipil",
        "x": 121.07010,
        "y": 14.65809,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Acacia",
        "x": 121.07016,
        "y": 14.65898,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Kalayaan",
        "x": 121.06911,
        "y": 14.65891,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Sanggumay",
        "x": 121.06784,
        "y": 14.65885,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Area 2",
        "x": 121.06777,
        "y": 14.66016,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "DiliMall",
        "x": 121.069492,
        "y": 14.659654,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "OUR",
        "x": 121.066434,
        "y": 14.651621,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "PHSD",
        "x": 121.07118,
        "y": 14.65890,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UHS",
        "x": 121.07102,
        "y": 14.65989,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Area 1",
        "x": 121.07061,
        "y": 14.66198,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UH",
        "x": 121.07286,
        "y": 14.66121,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CRL",
        "x": 121.07221,
        "y": 14.65984,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Int. Center",
        "x": 121.07331,
        "y": 14.65828,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Ilang Ilang",
        "x": 121.07345,
        "y": 14.65947,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Dagohoy",
        "x": 121.07418,
        "y": 14.66064,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "AC / GT",
        "x": 121.07378,
        "y": 14.65717,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IIS / RH",
        "x": 121.07303,
        "y": 14.65719,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Quezon Hall",
        "x": 121.06511,
        "y": 14.65487,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "PCED",
        "x": 121.07344,
        "y": 14.65620,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Virata",
        "x": 121.07348,
        "y": 14.65526,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Vinzons",
        "x": 121.07356,
        "y": 14.65439,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "SUB",
        "x": 121.07384,
        "y": 14.65420,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "KNL",
        "x": 121.06381,
        "y": 14.64725,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CFA",
        "x": 121.06179,
        "y": 14.65248,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "OCR",
        "x": 121.06012,
        "y": 14.65254,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "ASP",
        "x": 121.06323,
        "y": 14.65260,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "SPMO",
        "x": 121.06367,
        "y": 14.65194,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Gyud Food",
        "x": 121.06269,
        "y": 14.65188,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "HOA",
        "x": 121.06175,
        "y": 14.64971,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Kamagong",
        "x": 121.06263,
        "y": 14.64849,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Centennial",
        "x": 121.06265,
        "y": 14.64805,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Village B",
        "x": 121.06331,
        "y": 14.65104,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Village A",
        "x": 121.06331,
        "y": 14.64981,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Stat2",
        "x": 121.064324,
        "y": 14.651042,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "ARKI",
        "x": 121.06512,
        "y": 14.65108,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "STAT1",
        "x": 121.07113,
        "y": 14.65805,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CAL",
        "x": 121.06742,
        "y": 14.65266,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "ICE",
        "x": 121.06575,
        "y": 14.648678,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Track Oval",
        "x": 121.065917,
        "y": 14.659627,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "EEEP",
        "x": 121.06536,
        "y": 14.64943,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "MMM",
        "x": 121.06801,
        "y": 14.64829,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "EEEI",
        "x": 121.06830,
        "y": 14.64950,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CSLib",
        "x": 121.06942,
        "y": 14.64927,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NIGS",
        "x": 121.06946,
        "y": 14.64809,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "MSI",
        "x": 121.06909,
        "y": 14.65064,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NSRI",
        "x": 121.06911,
        "y": 14.65200,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NISMED",
        "x": 121.06756,
        "y": 14.65176,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "STC",
        "x": 121.067438,
        "y": 14.650377,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "VTC",
        "x": 121.061630,
        "y": 14.658126,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Cash Office",
        "x": 121.070304,
        "y": 14.660108 ,
        "rotation": 0,
        "fontsize": 4,
        "color": "black"
    },
    {
        "name": "7/11",
        "x": 121.067157,
        "y": 14.658041,
        "rotation": 0,
        "fontsize": 4,
        "color": "black"
    },
    {
        "name": "UPDPD & FD",
        "x": 121.065566,
        "y": 14.651984,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Vargas",
        "x": 121.06677,
        "y": 14.65335,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "AECH",
        "x": 121.06842,
        "y": 14.64852,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Palma Hall",
        "x": 121.06966,
        "y": 14.65282,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Arbo",
        "x": 121.06979,
        "y": 14.65080,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Kamia",
        "x": 121.070369,
        "y": 14.651852,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Sampaguita",
        "x": 121.07108,
        "y": 14.65207,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UPIS K-2",
        "x": 121.07224,
        "y": 14.65236,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UPIS 3-6",
        "x": 121.07219,
        "y": 14.65293,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "UPIS HS",
        "x": 121.07350,
        "y": 14.65314,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Benitez",
        "x": 121.07212,
        "y": 14.65354,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "Lagmay",
        "x": 121.07110,
        "y": 14.65354,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CHE",
        "x": 121.07331,
        "y": 14.65191,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "PAGASA",
        "x": 121.07245,
        "y": 14.65110,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IB",
        "x": 121.07087,
        "y": 14.65091,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NIMBB",
        "x": 121.07161,
        "y": 14.65072,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IC-R",
        "x": 121.07310,
        "y": 14.65091,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IC-T",
        "x": 121.07318,
        "y": 14.65028,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "NIP",
        "x": 121.07323,
        "y": 14.64893,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IMath",
        "x": 121.07156,
        "y": 14.64858,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "IESM",
        "x": 121.07025,
        "y": 14.64825,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CS Admin",
        "x": 121.070446,
        "y": 14.64977,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
        {
        "name": "Lagoon",
        "x": 121.06708,
        "y": 14.654930,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    },
    {
        "name": "CSRC",
        "x": 121.07131,
        "y": 14.64978,
        "rotation": 0,
        "fontsize": 5,
        "color": "black"
    }
    # Add more building labels...
]