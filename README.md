# Python TransIP

This is the Python client library for the TransIP API.

This client library is not officially supported by TransIP. The library should still be considered incomplete and in development mode. This means that breaking changing may be introduced in the next release.

## Documentation

The full documentation will follow shortly. The example below should give an impression of the possibilities:

```python
from transip import TransIP

# Demo token, for more information see:
# https://api.transip.nl/rest/docs.html#header-demo-token
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImN3MiFSbDU2eDNoUnkjelM4YmdOIn0.eyJpc3MiOiJhcGkudHJhbnNpcC5ubCIsImF1ZCI6ImFwaS50cmFuc2lwLm5sIiwianRpIjoiY3cyIVJsNTZ4M2hSeSN6UzhiZ04iLCJpYXQiOjE1ODIyMDE1NTAsIm5iZiI6MTU4MjIwMTU1MCwiZXhwIjoyMTE4NzQ1NTUwLCJjaWQiOiI2MDQ0OSIsInJvIjpmYWxzZSwiZ2siOmZhbHNlLCJrdiI6dHJ1ZX0.fYBWV4O5WPXxGuWG-vcrFWqmRHBm9yp0PHiYh_oAWxWxCaZX2Rf6WJfc13AxEeZ67-lY0TA2kSaOCp0PggBb_MGj73t4cH8gdwDJzANVxkiPL1Saqiw2NgZ3IHASJnisUWNnZp8HnrhLLe5ficvb1D9WOUOItmFC2ZgfGObNhlL2y-AMNLT4X7oNgrNTGm-mespo0jD_qH9dK5_evSzS3K8o03gu6p19jxfsnIh8TIVRvNdluYC2wo4qDl5EW5BEZ8OSuJ121ncOT1oRpzXB0cVZ9e5_UVAEr9X3f26_Eomg52-PjrgcRJ_jPIUYbrlo06KjjX2h0fzMr21ZE023Gw"

# Initialize a new TransIP API client
client = TransIP(access_token=ACCESS_TOKEN)

# List all domains in your account
domains = client.domains.list()
for domain in domains:
    print("Domain '{}' was registered at {}".format(domain.name, domain.registrationDate))

# List all vpss in your account
vpss = client.vpss.list()
for vps in vpss:
    print("VPS '{}' is {}".format(vps.name, vps.status))
```

## Installation

The installation instructions will follow shortly.

## Supported Python Versions

Python 3.6, 3.7, 3.8 and 3.9 are fully supported and tests. This library may work on later version of 3, but we do not currently run tests against those versions.

## Unsupported Python Version

Python < 3.6
## Third Party Libraries and Dependencies

The following libraries be we installed when you install the client library:

- [requests](https://github.com/psf/requests)

## Contributing

The contributing instructions will follow shortly.
