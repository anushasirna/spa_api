from fastapi import FastAPI
from faker import Faker
import random
import hashlib
from datetime import datetime, timedelta
import requests
import uuid
import uvicorn

app = FastAPI(title="SPA Activity API")

fake = Faker()

properties = {
    "RLC": "Red Lantern Casino",
    "BMC": "Blue Meridian Casino",
    "GPC": "Glass Palm Casino"
}

spa_services = [
    "Deep Tissue Massage",
    "Swedish Massage",
    "Hot Stone Therapy",
    "Facial Treatment",
    "Body Scrub",
    "Aromatherapy"
]

spa_products = [
    "Essential Oil",
    "Skin Care Kit",
    "Spa Candle",
    "Body Lotion",
    "Massage Cream"
]

actions = [
    "BOOK",
    "CHECK_IN",
    "CHECK_OUT",
    "ORDER",
    "CANCEL"
]

statuses = [
    "BOOK",
    "OPEN",
    "NOSH",
    "CANCEL",
    "PEND"
]

book_details = [
    "Deep 50, Ultimate Wrap 60",
    "Deluxe 50 min, Hydra Eye Treatment, WCWM Mani/ Pedi Comb",
    "Diamond Glass Facical Weekend, ManDatory Facial Weekend",
    "French Mani/Pedi, Paraffin Hands & Fee",
    "Deluxe 50 min, Paraffin Hands & Fee, Swedish 80",
    "Microcurrent lift, WCW Pedi 50",
    "50 Min Facial, BACK WAX",
    "Paraffin Hands & Fee, WCW Pedi 50, Wind Creek's Peacefu",
    "Full Legs Hair Remov, No Botox Facial 80 m"
]

order_details = [
    "Hydra Eye Treatment",
    "Spa Product Kit",
    "Essential Oil Package",
    "Premium Facial Add-on",
    "Luxury Massage Oil",
    "Aromatherapy Package",
    "Body Scrub Combo"
]

cancel_reasons = [
    "No Show",
    "Card on file did not go through",
    "CC on file declined",
    "Changed Mind",
    "Called at 9:18am to cancel",
    "Canceled due to technology issues this morning. Extend credits for September.",
    "24 hrs Cancellation she rebooked for 7/25",
    "couples tub is down",
    "User Error  tour got overtimed",
    "3rd person has to work",
    "Cm Training",
    "Other - Please specify"
]

checkin_details = [
    "Guest arrived for scheduled treatment",
    "Customer checked in successfully",
    "Spa access activated",
    "Treatment room assigned",
    "Guest verified at front desk"
]

checkout_details = [
    "Service completed successfully",
    "Guest checked out from spa",
    "Payment completed",
    "Spa session closed",
    "Checkout completed with gratuity"
]

def generate_person_id(activeclubid):

    return str(
        int(
            hashlib.md5(
              ('spa' + activeclubid).encode()
            ).hexdigest(),
            16
        ) % 90000 + 10000
    )


def generate_base_spa_booking(activeclubid):

    person_id = generate_person_id(
        activeclubid
    )

    property_code = random.choice(
        list(properties.keys())
    )

    property_name = properties[
        property_code
    ]

    booking_id = fake.uuid4()

    booking_number = fake.numerify(
        "SPA########"
    )

    booking_date = (
        datetime.now()
        - timedelta(
            days=random.randint(1, 30)
        )
    )

    checkin_date = (
        booking_date
        + timedelta(
            days=random.randint(0, 3)
        )
    )

    checkout_date = (
        checkin_date
        + timedelta(
            hours=random.randint(1, 5)
        )
    )

    gaming_date = booking_date.date()

    duration = random.randint(
        30,
        180
    )

    transaction_amount = round(
        random.uniform(50, 1000),
        2
    )

    player_value = round(
        transaction_amount * random.uniform(0.1, 0.5),
        2
    )


    activity_details = [
    {
        "activity_actual_price":
            round(
                random.uniform(50, 300),
                2
            ),

        "activity_id":
            random.randint(
                100,
                999
            ),

        "activity_name":
            random.choice(
                spa_services
            ),

        "activity_price":
            round(
                random.uniform(50, 300),
                2
            ),

        "activity_type":
            random.choice(
                ["A", "B", "C"]
            )
    }
]

    product_details = [
        {
            "product_actual_price":
                round(
                    random.uniform(10, 150),
                    2
                ),

            "product_id":
                random.randint(
                    1000,
                    9999
                ),

            "product_name":
                random.choice(
                    spa_products
                ),

            "product_price":
                        round(
                            random.uniform(10, 150),
                            2
                        ),

                    "product_line":
                        "P"
                }
            ]

    transaction_amount = (
        sum(
            item["activity_price"]
            for item in activity_details
        )
        +
        sum(
            item["product_price"]
            for item in product_details
        )
    )

    
    return {

        

        "PERSON_ID":
            person_id,

        "ACTIVE_CLUB_ID":
            activeclubid,

        "SOURCE":
            "SPA_SYSTEM",

        "ENTITY":
            "SPA",

        "EVENT_GROUP_ID":
            str(uuid.uuid4()),

        "PROPERTY_NAME":
            property_name,

        "PROPERTY_CODE":
            property_code,

        

        "SPA_BOOKING_ID":
            booking_id,

        "SPA_BOOKING_NUMBER":
            booking_number,

        "BOOKING_DATE":
            booking_date,

        "CHECKIN_DATE":
            checkin_date,

        "CHECKOUT_DATE":
            checkout_date,

        "GAMING_DATE":
            gaming_date.isoformat(),

        "DURATION":
            duration,

        "TRANSACTION_AMOUNT":
            transaction_amount,

        "PLAYER_VALUE":
            player_value,

        "SPA_ACTIVITY_DURATION":
            duration,

        "SPA_ACTIVITY_DETAILS": activity_details,

        "SPA_PRODUCT_DETAILS": product_details,

        

        "SPA_DISCOUNT_AMOUNT":
            round(
                random.uniform(0, 50),
                2
            ),

        "SPA_GRATUITY_AMOUNT":
            round(
                random.uniform(5, 50),
                2
            ),

        "SPA_TAX_AMOUNT":
            round(
                random.uniform(5, 25),
                2
            ),

        "SPA_TIP_AMOUNT":
            round(
                random.uniform(5, 40),
                2
            ),

        "SPA_ACTIVITY_CANCEL_REASON":
            None,

        "EVENT_TIMESTAMP_PROPERTY":
            booking_date.isoformat(),

        "EVENT_TIMESTAMP_PROPERTY_TIMEZONE":
            "America/New_York",

        "GAMING_DATE_TIMEZONE":
            "America/New_York",

        

        "LOAD_TIMESTAMP":
            datetime.now().isoformat()
    }


def build_spa_event(
    booking_data,
    action,
    status
):

    record = booking_data.copy()

    event_timestamp = (
        record["BOOKING_DATE"]
    )

    if action == "CHECK_IN":

        event_timestamp = (
            record["CHECKIN_DATE"]
        )

    elif action == "CHECK_OUT":

        event_timestamp = (
            record["CHECKOUT_DATE"]
        )

    elif action == "ORDER":

        event_timestamp = (
            record["CHECKIN_DATE"]
            + timedelta(
                minutes=random.randint(
                    10,
                    120
                )
            )
        )

    elif action == "CANCEL":

        event_timestamp = (
            record["BOOKING_DATE"]
            + timedelta(
                days=random.randint(
                    1,
                    5
                )
            )
        )

    if action == "ORDER":

        status = None

    if action == "CANCEL":

        record[
            "SPA_ACTIVITY_CANCEL_REASON"
        ] = random.choice([
            "Customer Request",
            "No Availability",
            "Payment Failure",
            "Emergency"
        ])

    detail_value = None

    if action == "BOOK":

        detail_value = random.choice(
            book_details
        )

    elif action == "ORDER":

        detail_value = random.choice(
            order_details
        )

    elif action == "CHECK_IN":

        detail_value = random.choice(
            checkin_details
        )

    elif action == "CHECK_OUT":

        detail_value = random.choice(
            checkout_details
        )

    elif action == "CANCEL":

        detail_value = random.choice(
            cancel_reasons
        )

    return {

        "EVENT_TIMESTAMP":
            event_timestamp.isoformat(),

        "EVENT_TIMESTAMP_PROPERTY":
            event_timestamp.isoformat(),

        "EVENT_TIMESTAMP_PROPERTY_TIMEZONE":
            record[
                "EVENT_TIMESTAMP_PROPERTY_TIMEZONE"
            ],

        "DURATION":
            record["DURATION"],

        "GAMING_DATE":
            event_timestamp.date().isoformat(),

        "GAMING_DATE_TIMEZONE":
            record[
                "GAMING_DATE_TIMEZONE"
            ],

        

        "PERSON_ID":
            record["PERSON_ID"],

        "ACTIVE_CLUB_ID":
            record["ACTIVE_CLUB_ID"],

        "SOURCE":
            record["SOURCE"],

        "ENTITY":
            record["ENTITY"],

        "ACTION":
            action,

        "ENTITY_ACTION":
            f"SPA:{action}",

        "DETAILS":
            detail_value,

        "EVENT_ID":
            str(uuid.uuid4()),

        "EVENT_GROUP_ID":
            record["EVENT_GROUP_ID"],

        "PROPERTY_NAME":
            record["PROPERTY_NAME"],

        "PROPERTY_CODE":
            record["PROPERTY_CODE"],

        
        "TRANSACTION_AMOUNT":
            (
                record["TRANSACTION_AMOUNT"]
                if action == "ORDER"
        else None
            ),

        "PLAYER_VALUE":
            (
                record["PLAYER_VALUE"]
                if action == "ORDER"
        else None
            ),

        "SPA_BOOKING_ID":
            record["SPA_BOOKING_ID"],

        "SPA_BOOKING_NUMBER":
            record["SPA_BOOKING_NUMBER"],

        "SPA_BOOKING_STATUS":
            status,

        "SPA_ACTIVITY_DURATION":
            record[
                "SPA_ACTIVITY_DURATION"
            ],
    

        "SPA_ACTIVITY_CANCEL_REASON":
                (
            detail_value
            if action == "CANCEL"
            else None
        ),

        "SPA_DISCOUNT_AMOUNT":
                (
            record["SPA_DISCOUNT_AMOUNT"]
            if action == "ORDER"
            else None
        ),

        "SPA_GRATUITY_AMOUNT":
                (
            record["SPA_GRATUITY_AMOUNT"]
            if action == "ORDER"
            else None
        ),

        "SPA_TAX_AMOUNT":
                (
            record["SPA_TAX_AMOUNT"]
            if action == "ORDER"
            else None
        ),

        "SPA_TIP_AMOUNT":
                (
            record["SPA_TIP_AMOUNT"]
            if action == "ORDER"
            else None
        ),

        "SPA_ACTIVITY_DETAILS":
            record[
                "SPA_ACTIVITY_DETAILS"
            ],

        "SPA_PRODUCT_DETAILS":
            (
                record[
                    "SPA_PRODUCT_DETAILS"
                ]
                if action == "ORDER"
                else None
            ),

        

        

        "LOAD_TIMESTAMP":
            datetime.now().isoformat()
    }


@app.get("/v1/spa-activity")
async def spa_activity():

    api_url = (
        "https://casino-api-ob26.onrender.com/"
        "v1/player-activity"
    )

    response = requests.get(
        api_url
    )

    player_data = response.json()

    unique_activeclubids = []

    seen = set()

    for row in player_data:

        activeclubid = row[
            "ACTIVECLUBID"
        ]

        if activeclubid not in seen:

            seen.add(
                activeclubid
            )

            unique_activeclubids.append(
                activeclubid
            )

        if len(unique_activeclubids) == 50:
            break

    final_records = []

    for index, activeclubid in enumerate(
        unique_activeclubids
    ):

        booking_data = (
            generate_base_spa_booking(
                activeclubid
            )
        )

        booking_status = random.choice(
            statuses
        )

        # ------------------------------------------------
        # FLOW 1
        # BOOK -> CHECK_IN -> ORDER -> CHECK_OUT
        # ------------------------------------------------

        final_records.append(
            build_spa_event(
                booking_data,
                "BOOK",
                booking_status
            )
        )

        final_records.append(
            build_spa_event(
                booking_data,
                "CHECK_IN",
                random.choice(statuses)
            )
        )

        

        

        final_records.append(
            build_spa_event(
                booking_data,
                "ORDER",
                None
            )
        )

        final_records.append(
            build_spa_event(
                booking_data,
                "CHECK_OUT",
                random.choice(statuses)
            )
        )

        # ------------------------------------------------
        # FLOW 2
        # BOOK -> CANCEL
        # ------------------------------------------------

        if index < 20:

            cancel_booking_data = (
                generate_base_spa_booking(
                    activeclubid
                )
            )
            cancel_booking_data[
                "DURATION"
            ] = 0

            cancel_booking_data[
                "SPA_ACTIVITY_DURATION"
            ] = 0

            final_records.append(
                build_spa_event(
                    cancel_booking_data,
                    "BOOK",
                    "CANCEL"
                )
            )

            final_records.append(
                build_spa_event(
                    cancel_booking_data,
                    "CANCEL",
                    "CANCEL"
                )
            )

    return final_records


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003
    )
