# PLP - PiletiLevi Printing

Two types of PLP files are supported

## PLP with fiscal data

**Example fiscal end shift**
    {
        "info": "fiscal",
        "salesPoint": "* Bilietai BO",
        "operation": "endshift",
        "version": "1.0.2"
    }

**Example fiscal start shift**
    {
        "info": "fiscal",
        "salesPoint": "* Bilietai BO",
        "operation": "startshift",
        "version": "1.0.2"
    }

**Example fiscal data**

    {
        "info": "fiscal",
        "version": "1.0.2",
        "printerName": "COM4",
        "printerType": "fiscal",
        "operation": "sale",
        "salesPoint": "* Bilietai BO",
        "payments": [
            {
                "type": "3",
                "cost": 10.00,
                "components": [
                    {
                        "type": "tickets",
                        "name": "Bilietai",
                        "cost": 1.60,
                        "kkm": true,
                        "vatPerc": 0.00
                    }, {
                        "type": "service fee",
                        "amount": 8,
                        "name": "Test mokestis BT",
                        "cost": 7.20,
                        "kkm": true,
                        "vatPerc": 20
                    }, {
                        "type": "service fee",
                        "amount": 8,
                        "name": "Pardavimo punkto mokestis",
                        "cost": 1.20,
                        "kkm": true,
                        "vatPerc": 20
                    }
                ]
            }, {
                "type": "1",
                "cost": 3.60,
                "components": [
                    {
                        "type": "service fee",
                        "amount": 8,
                        "name": "Pardavimo punkto mokestis",
                        "cost": 3.60,
                        "kkm": true,
                        "vatPerc": 20
                    }
                ]
            }
        ]
    }

## PLP with ticket information
**Example**

    {
        "info": "tickets",
        "printerName": "Godex DT4x",
        "printerType": "fiscal",
        "operation": "sale",
        "salesPoint": "* Bilietai BO",
        "blankType": "B_balt_152x70",
        "version": "1.0.2",
        "documents": [
            {
                "aeg": "9. september 2011",
                "layout": "http://www.piletilevi.ee/layouts/default.pla",
                "lisatext1": "Piletilevi ja BTH poolt:",
                "lisatunnus": "0310302000",
                "piletid1": "27859650",
                "piletid2": "27859650",
                "piletiliik1": "KUTSE",
                "piletiliik2": "K",
                "piltleft": "left_1252403227_veneteater_150x245.jpg",
                "sektor1": "KINO",
                "sektor2": "KINO",
                "toimkoht": "Tallinnas,",
                "triipid": "96960310650437",
                "yritus1": "PALJU ÕNNE!",
                "yritus2": "150 Eurot E-lugeri soetamiseks"
            },
            {
                "aeg": "9. september 2011",
                "layout": "http://www.piletilevi.ee/layouts/default.pla",
                "lisatext1": "Piletilevi ja BTH poolt:",
                "lisatunnus": "0310302000",
                "piletid1": "27859651",
                "piletid2": "27859651",
                "piletiliik1": "KUTSE",
                "piletiliik2": "K",
                "piltleft": "left_1252403227_veneteater_150x245.jpg",
                "sektor1": "KINO",
                "sektor2": "KINO",
                "toimkoht": "Tallinnas,",
                "triipid": "71960310651283",
                "yritus1": "PALJU ÕNNE!",
                "yritus2": "150 Eurot E-lugeri soetamiseks"
            },
            {
                "aeg": "9. september 2011",
                "layout": "http://www.piletilevi.ee/layouts/default.pla",
                "lisatext1": "Piletilevi ja BTH poolt:",
                "lisatunnus": "0310302000",
                "piletid1": "27859652",
                "piletid2": "27859652",
                "piletiliik1": "KUTSE",
                "piletiliik2": "K",
                "piltleft": "left_1252403227_veneteater_150x245.jpg",
                "sektor1": "KINO",
                "sektor2": "KINO",
                "toimkoht": "Tallinnas,",
                "triipid": "24960310652580",
                "yritus1": "PALJU ÕNNE!",
                "yritus2": "150 Eurot E-lugeri soetamiseks"
            }
        ]
    }
