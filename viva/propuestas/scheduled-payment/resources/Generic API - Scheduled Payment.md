# Generic API \- Scheduled Payment

# 0. Document Status

| Field | Value |
| --- | --- |
| Status | READY FOR DEV |
| Tech Lead | Héctor Rodríguez |
| Target Epic | Generic: [API-1994](https://vivaaerobus.atlassian.net/browse/API-1994) |
| Ready for Dev? | YES |
| Last updated | 2026-11-13 |

# 1. Business Context REQUIRED

## 1.1 General statement

Create a booking without paying the TUA now. The TUA is charged later by a separate batch process, which is out of the scope of this document.

Generic API only needs to do two things in `POST /Payment/Process`:

1. Accept a new flag, `scheduledTuaPayment = true`, in the request.
2. After Navitaire confirms the payment, call Adyen `listRecurringDetails` to get the `FirstPspReference` and save it in the note of a new SSR, `VTUP`.

The three scenarios work in a similar way (see the sequence diagram); only the content of the SSR note changes. A single payment processor (Adyen) is used.

This document contains only the scope for Generic API.

## 1.2 Users / personas affected

| Account type | Eligible? | Notes |
| --- | --- | --- |
| Anonymous | Yes | Scenario 1 |
| Customer | Yes | Scenarios 1, 2 and 3 |
| Agency | No |   |
| Staff | No |   |
| Enterprise | No |   |

## 1.3 Scope

### Flows in scope

| Flow | In scope? | Notes |
| --- | --- | --- |
| Booking | Yes | Reservation creation (`POST /Payment/Process`) |
| Manage | No |   |
| Check-in | No |   |
| Transfer | No |   |

### Booking types in scope

| Booking type | In scope? | Notes |
| --- | --- | --- |
| Regular | Yes |   |
| Points | No |   |
| RegularAndPoints | Yes |   |
| Event | No |   |

### Impacted features IF APPLICABLE

| Feature | Impact | Notes |
| --- | --- | --- |
| TUA | Logic change | A new SSR, `VTUP`, is created after the payment. The existing pay-later SSR (VTUB) is not changed. |
| Rest of the features | No |   |

## 1.4 UI / Figma IF APPLICABLE

\\\<\<<https://www.figma.com/design/37mnOFV8J5deGKEdNqdfSM/Tualiado-5.0?node-id=1619-71226&t=tNH9BPKzrwCE96jE-1> \> \\\>

# 2. Sequence Diagram REQUIRED

## 2.1 Reservation creation — `POST /Payment/Process`, one flow per scenario

The sequence diagram has 3 scenarios with the Adyen integration:

1. **Scenario 1:** CardPayment, new card, storeCard = false (one time payment)
2. **Scenario 2:** CardPayment, new card, storeCard = true (customer: logged-in user)
3. **Scenario 3:** StoredPayment (logged-in user)

Sequence diagram:

# 3. Admin Portal Configuration IF APPLICABLE

| Toggle / setting name | Behavior when ON | Behavior when OFF | Default state | Notes |
| --- | --- | --- | --- | --- |
| `scheduledTuaPayment.enabled`This setting should be added inside “Mexico Departure Tax” section on the Customer Services AP Page | The flag `scheduledTuaPayment` is accepted and processed | Current flow, no VTUP |   |  |

# 4. API Changes REQUIRED

## 4.1 `/Payment/Process` — MODIFIED ENDPOINT

| Field | Value |
| --- | --- |
| URL | `/Payment/Process` |
| Method | POST |
| Flows affected | Booking |
| Change type | Modified |

### Execution Steps

| Step | Activity | Details |
| --- | --- | --- |
| 1 | Receive the flag `scheduledTuaPayment` | Prerequisites: - `scheduledTuaPayment = true` - Actual pay now TUA SSR VTUA/VTUI is not added - TUA is not included in a fare - TUA is applicable for at least one journey (Mexican origin airport, no EVT/TVT, not Iberia carrier, etc.) else execute legacy flow. |
| 2 | Get the `FirstPspReference` | After the payment is successfully processed in Navitaire, call Adyen `listRecurringDetails` with the shopper reference of the payment: `basketId` in scenario 1, customer number in scenarios 2 and 3. Take the `FirstPspReference` of the card used in the payment, as defined in Business Rules: <https://vivaaerobus.atlassian.net/wiki/spaces/REQ/pages/4893016079/Generic+API+-+Scheduled+Payment#Business-Rules-for-SSR-note%3A> |
| 3 | Create the new VTUP SSR | Create the SSR `VTUP` in Navitaire and save the SSR note as defined in the next table. Return the existing response (reservation created, TUA pending). |

#### Business Rules for SSR note:

SSR note of `VTUP`:

| Scenario | SSR note |
| --- | --- |
| 1 - CardPayment, new card, storeCard = false | `basketid+FirstPspReference` |
| 2 - CardPayment, new card, storeCard = true | `customerid+FirstPspReference` |
| 3 - StoredPayment | `customerid+FirstPspReference` |

How the card used in the payment is identified in the `listRecurringDetails` response:

| Scenario | Card used in the payment |
| --- | --- |
| 1 | The response always has a single card. The shopper reference is the `basketId`, and an active basket can be used only once to create a reservation, so a basket has only one tokenized card (one `FirstPspReference`) |
| 2 | Try to use de “`alias`” to get the `FirstPspReference`. If generic can’t get this value for this scenario, use the next data of the adyen response: `additionalData.cardBin` and `card.number` (last digits of the card) match the BIN and the last digits of the card number sent in `cardPayload` of the `payment/process`. The combination of both values identifies the card among the cards of the shopper reference. |
| 3 | The entry whose `alias` is equal to the `storedPaymentKey` sent in `cardPayload`. The `alias` is the identifier Adyen assigns to a tokenized card; Generic API already uses it as `storedPaymentKey`. |

Contract type:

`UnscheduledCardOnFile` (payment field `ADYEN::ContractType`) is sent in the payment only when `scheduledTuaPayment = true`. When the flag is false or absent, the payment fields are the existing ones and nothing changes (send: `{\"key\":\"ADYEN::ContractType\",\"value\":\"ONECLICK\"}`.

`listRecurringDetails` is requested with the `shopperReference` and the merchant account only, with no contract filter. Adyen returns all the cards stored for that shopper reference 

### Generic API: Client-Facing Contract

#### Request

```json
// Only the new field is shown. The rest of the request is unchanged.
{
  "scheduledTuaPayment": true // NEW
}
```

#### Request field definitions

| Field name | Type | Required? | Allowed values | Default if absent | Description |
| --- | --- | --- | --- | --- | --- |
| `scheduledTuaPayment` | bool | No | true, false | false | The TUA is not charged now. It will be charged later by the batch process. |

### Adyen Integration

#### Adyen: list the stored cards

| Field | Value |
| --- | --- |
| External service | Adyen |
| Endpoint / operation | `POST /pal/servlet/Recurring/v49/listRecurringDetails` |
| Triggered when | `scheduledTuaPayment = true` and the payment was successfully processed in Navitaire |

**Request sent to Adyen**

```json
{
  "shopperReference": "basketId (scenario 1) | customerNumber (scenarios 2 and 3)",
  "merchantAccount": "VB_WEB"   // Adyen returns all the cards stored for this merchant account and shopper reference
}
```

**Response received from Adyen**

```json
{
    "shopperReference": "3290129706",
    "details": [
        {
            "RecurringDetail": {
                "alias": "M177654806491264",
                "contractTypes": [
                    "ONECLICK",
                    "RECURRING"
                ],
                "creationDate": "2025-12-17T16:28:29+01:00",
                "card": {
                    "number": "7643"
                },
                "additionalData": {
                    "cardBin": "540956"
                },
                "firstPspReference": "LK644CFNRQ85FNV5",
                "recurringDetailReference": "*HPT5"
            }
        },
        {
            "RecurringDetail": {
                "alias": "E328049113056958",
                "contractTypes": [
                    "ONECLICK",
                    "RECURRING"
                ],
                "creationDate": "2026-03-27T18:31:02+01:00",
                "card": {
                    "number": "1111"
                },
                "additionalData": {
                    "cardBin": "444433"
                },
                "firstPspReference": "TR2K4BZVSVQTWBV5",
                "recurringDetailReference": "*XWV5"
            }
        }
    ]
}

// Only the fields used are shown, with two cards of the real response as example. Scenario 2: the entry whose cardBin and card.number match the card of the payment (here 540956 and 7643) gives the FirstPspReference, if generic can't get with alias field. Scenario 3: the entry whose alias is the storedPaymentKey of the payment (for example M177654806491264) gives the FirstPspReference (LK644CFNRQ85FNV5).
```

### Navitaire: create the VTUP SSR

| Field | Value |
| --- | --- |
| External service | Navitaire |
| Endpoint / operation | `ssrsAddManual` |
| Triggered when | `scheduledTuaPayment = true` and `FirstPspReference` was obtained |

**Request sent to Navitaire**

```json
{
  "requests": [ {
    "type": "Journey",
    "items": [ { "ssrCode": "VTUP", "passengerKey": "...", "count": 1, "note": "basketid|FirstPspReference (scenario 1) | FirstPspReference (scenarios 2 and 3)" } ]
  } ]
}
```

 

### Acceptance Criteria

- Given a payment with a new card that is not saved (scenario 1) and `scheduledTuaPayment = true`, when the payment succeeds, then the booking has the SSR `VTUP` with the note `basketid|FirstPspReference`.
- Given a payment with a new card that is saved (scenario 2) and `scheduledTuaPayment = true`, when the payment succeeds, then the booking has the SSR `VTUP` with the note `FirstPspReference` and `customerNumber` of the entry whose `cardBin` and `card.number` match the card of the payment.
- Given a payment with a stored card (scenario 3) and `scheduledTuaPayment = true`, when the payment succeeds, then the booking has the SSR `VTUP` with the note `FirstPspReference` and `customerNumber`of the entry whose `alias` is the `storedPaymentKey` of the payment.
- Given a payment without `scheduledTuaPayment`, then the flow is unchanged and no `VTUP` is created.

**Length of the SSR note.** The SSR note allows a maximum of 128 characters. Adyen confirmed that its references, including the one tied to the basket, are 16 characters long, so the note of scenario 1 (`basketid|FirstPspReference`) fits in the 128 characters, and so do the notes of scenarios 2 and 3.

**TUA amount: **The TUA has no changes in this process. It is already saved in the booking comments, before the commit, with the format `TUA|out|in|total` (for example `TUA|652.95|0|652.95`). The batch process reads it from the booking (retrieve in Navitaire) to process the correct amount.

### Test Matrix

| # | Scenario type | Test case description | Expected Result | Execution |
| --- | --- | --- | --- | --- |
| 1 | Happy path | **Scenario 1:**config: `scheduledTuaPayment.enabled`Steps:Create new booking flow (search journeys \> create basket \> add journeys to basket \> select bundle \> passengers \> get payment methods) and pay with: `CardPayment`, `storeCard` false, `scheduledTuaPayment` true | `VTUP` with note `FirstPspReference` and `basketid`Payment Fields: `{ "fields": { "ADYEN::ContractType": "", "ADYEN::ShopperReference": "", "Avs::Address1": "", "Avs::City": "", "Avs::Country": "", "Avs::PostalCode": "", "Avs::StateOrProvince": "", "BillTo::Email": "", "BillTo::FirstName": "", "BillTo::IPAddress": "",  "BillTo::LastName": "", "BillTo::Phone": "", "Browser::SessionID": "", "CardType": "", "CC::CarrierCode": "", "FPS::DeviceFingerprintID": "", "FPS::Enabled": "", "FPS::MDF1": "", "FPS::MDF10": "", "FPS::MDF11": "", "FPS::MDF12": "", "FPS::MDF13": "", "FPS::MDF14": "", "FPS::MDF15": "", "FPS::MDF16": "", "FPS::MDF18": "", "FPS::MDF19": "", "FPS::MDF4": "", "FPS::MDF5": "", "FPS::MDF6": "", "FPS::MDF7": "", "FPS::MDF8": "", "FPS::MDF9": "", "Issuer": "", "NS::AgentName": "", "NS::AgentRole": "", "OriginalLocation": "", "SP:PAYID": "", "TransactionTypeIndicator": ""   } }` | AUTOMATED |
| 2 | Happy path | **Scenario 2:**config:`scheduledTuaPayment.enabled`Steps:Create new booking flow (search journeys \> create basket \> add journeys to basket \> select bundle \> passengers \> get payment methods) and pay with:`CardPayment`, `storeCard` true, `scheduledTuaPayment` true | `VTUP` with note `FirstPspReference` and `cumstomerNumber`Payment Fields:`{   "fields": { "ADYEN::ContractType": "", "ADYEN::ShopperReference": "", "Avs::Address1": "", "Avs::City": "", "Avs::Country": "", "Avs::PostalCode": "", "Avs::StateOrProvince": "", "BillTo::Email": "", "BillTo::FirstName": "", "BillTo::IPAddress": "", "BillTo::LastName": "", "BillTo::Phone": "",    "Browser::SessionID": "", "CardType": "", "CC::CarrierCode": "", "FPS::DeviceFingerprintID": "", "FPS::Enabled": "", "FPS::MDF1": "",    "FPS::MDF10": "", "FPS::MDF11": "", "FPS::MDF12": "", "FPS::MDF13": "", "FPS::MDF14": "",  "FPS::MDF15": "",  "FPS::MDF16": "", "FPS::MDF18": "", "FPS::MDF19": "", "FPS::MDF4": "", "FPS::MDF5": "", "FPS::MDF6": "", "FPS::MDF7": "", "FPS::MDF8": "", "FPS::MDF9": "", "Issuer": "", "NS::AgentName": "", "NS::AgentRole": "", "OriginalLocation": "", "SP:PAYID": "", "TransactionTypeIndicator": ""   } }` | AUTOMATED |
| 3 | Happy path | **Scenario 3:**Config:`scheduledTuaPayment.enabled`Steps:Create new booking flow (search journeys \> create basket \> add journeys to basket \> select bundle \> passengers \> get payment methods) and pay with:`StoredPayment`, `scheduledTuaPayment` true | `VTUP` with note `FirstPspReference` and `cumstomerNumber`payment fields: `{ "fields": { "ADYEN::ContractPAN": "", "ADYEN::ContractType": "", "ADYEN::ShopperReference": "", "BillTo::Email": "", "BillTo::IPAddress": "",    "BIN": "", "CC::CarrierCode": "", "DIGT": "", "FPS::Enabled": "",    "FPS::MDF1": "", "FPS::MDF10": "", "FPS::MDF11": "",  "FPS::MDF12": "", "FPS::MDF13": "",  "FPS::MDF14": "",  "FPS::MDF15": "", "FPS::MDF16": "", "FPS::MDF18": "", "FPS::MDF19": "", "FPS::MDF4": "", "FPS::MDF5": "", "FPS::MDF6": "", "FPS::MDF8": "", "MARCA": "", "NS::AgentName": "",    "NS::AgentRole": "", "OriginalLocation": "", "SP:PAYID": "", "TransactionTypeIndicator": ""   } }` | AUTOMATED |
| 4 | Regression | Config:`scheduledTuaPayment.disabled`Steps:Create new booking flow (search journeys \> create basket \> add journeys to basket \> select bundle \> passengers \> get payment methods) and pay with:Card payment and stored payment without `scheduledTuaPayment` | Current behavior unchanged | AUTOMATED |

### Dependencies

| Dependency | Team / system | What is needed | **Status** |
| --- | --- | --- | --- |
| Navitaire | Navitaire | Create the SSR code `VTUP`, with no charge to the booking | In Progress |
| MMB Flow | Frontend | Confirm the behavior upon manual deletion of the SSRs (VTUB, VTUI). | In Progress |
