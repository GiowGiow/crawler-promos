A deal has the following structure:
- Type (DEAL, COUPON, etc)
- ID
- Title
- Description (Generally some HTML)
- CrawledFrom:
    - ID
    - Source Name (Pelando, Hardmob, etc)
    - URL
- Optional:
    - URL of the deal
    - Coupon Code
    - Expiry Date
    - Fixed Discount
    - Percentage Discount
    - Free Shipping
    - Image
    - Local Deal (eg. in Brazil)
    - Score
    - Store
    - Price
    - Status (Active, Inactive)
- Comment: (optional)
    - Comment count
    - Featured comment
    - Last Comment
    - Last Comment Timestamp
- Timestamp (in UNIX timestamp):
    - Created Time (optional)
    - Crawled Time

## JSON Example
```
{
    "id": "SOME_GENERATED_ID",
    "title": "Some title",
    "description": "SOME_POST_HTML",
    "type": "DEAL",
    "crawledFrom": {
        id: "SOME_ID",
        sourceName: "Pelando",
        url: "https://www.pelando.com/some-id-url"
    },
    "optional": {
        "dealUrl": "HTTP://SOME_URL",
        "couponCode": null,
        "expiryDate": null,
        "discountFixed": null,
        "discountPercentage": null,
        "freeShipping": null,
        "image": "url",
        "fromBrazil": null,
        "score": SOME_VALUE
        "store": null,
        "price": 0,
        "status": "ACTIVE",
    },
    "comment": {
        "commentCount": 0,
        "featuredComment": null,
        "lastComment": null,
        "lastCommentedAt": "SOME_TIMESTAMP"
    },
    "timestamps": {
        "created": "UNIX_TIME_STAMP",
        "crawled": "UNIX_TIME_STAMP"
    },
}
```
