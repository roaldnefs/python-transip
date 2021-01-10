# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, 2021 Roald Nefs <info@roaldnefs.com>
#
# This file is part of python-transip.
#
# python-transip is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-transip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-transip.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import responses  # type: ignore

from transip import TransIP
from tests.utils import load_responses_fixtures


class TransIPTest(unittest.TestCase):
    """Test the TransIP client class."""

    client: TransIP
    privkey: str

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a minimal TransIP client and RSA private key."""
        cls.client = TransIP(access_token='ACCESS_TOKEN')
        cls.privkey: str = (  # type: ignore
            "-----BEGIN RSA PRIVATE KEY-----\n"
            "MIIEpAIBAAKCAQEAsUSEHsMuB380OUZQWDyyND4q8lEuJAgNnMkO8s5NGwzP8XSi\n"
            "2DdFglLGLe9kjpADs3XqZFsk8ZFFn7x0idFydGyh9tbJ2WkR9E+kNUJV5iQDzPOB\n"
            "wvyygEREqnl/o1h3c1q8tD2HZKBcjChn9JbMzdWwAaIs3ppcGWrEI0jZFFfSAyIZ\n"
            "GkC3k3umOykWIKflQcT/soAfdqW+2P9/KD/wb3AZCer2i6B2hiITiDbHh5q84Hgk\n"
            "D/Zg1M4yrYDyxDeGkAJHkGKNaE0tgUPoz3XTGP7uFYIx00qJyhmnzQcyV/Xcw3ZQ\n"
            "7DFUj1HQ5wG/kEF9a4F1+AAiO5C5QbGTFYSwBwIDAQABAoIBABbtIZlI7P8TOJHf\n"
            "wixnTTTshWlpjmoikIAikMheXiKNeadkylrkaxz7z53JRFwbzB69tV7dWt3TSAns\n"
            "ubXJXOAp3JisFtcDe8r5MeeheLKXHda396RcQknMioTxycw6eNh2d8ln28br5oxJ\n"
            "/YfoqPxGEsljTCJOHHM9F7johwrWSQ6f+gmiOkABvIHKgTBLa++v0D+vNrUjM6rx\n"
            "IE+dBrx8yIgkF4qSg4Dqnr7D0KqCZUGLZ/3K8ShQUtiQYzyHIWKUId3NUecIQcrT\n"
            "2Ri2TITKuER0fa7Mr+3LMSh/3+HtP2AoM34ouxr9H98LFz/UXxuFIRFTx7UVRt4N\n"
            "3zqhsEECgYEA+TnXanBJmFz3sNYtlQixtKrh496GB0NheuK4xeNEj9/3gJ6J/rtL\n"
            "ZHI7VH8r6aqoqw7sO/WJdxkwZTBOz2fe1QJ5BN0HBI5S6jIBQv9Nfqar0TDvNLB+\n"
            "pH6eYJZ/IEFIMObv9YmsPohXpGeXynecrpl8SazEIWLb8IzgLY0HpokCgYEAthX5\n"
            "1th4Re0P9rzXp21bbEwcvOKcg5dcpSaTtA1eQEILl6qqT3FP7w8/Ed7NRRY9Gcs+\n"
            "inAc96YRNAgIGgfT3R1BmxOMWfdFBT1zlCheS6egKKLzVPzKPiMoMP4zu4hy6uH5\n"
            "YVqpDLu0YQu1J2L0VYdZ9xAC0//Rx8KRcs6m/g8CgYEA41VDja+HMhf7R67WPU+E\n"
            "6YvGKRjdoNpxnKoaaUd5TtO46/WxYk5t4t3gCJ9H6wjkecRO8BJ0pdKwNlzuRno0\n"
            "5JAw26LRt/Iq571dMUO36IMXzuWYDLPBkUJ+LRSaOU3TD+hXkd1W5GNxrmFgMCsT\n"
            "HKCcooeZD+shPDcEdghipiECgYARBTDbYlSrxKMPX0uRPOmkz+CHz27t5gIk9dws\n"
            "omtC+ml2/d75mg/surIci4UIhjGj7Zmk+yHaDE3jXTTUqhKlwoxVYJhn+HMdMEdT\n"
            "fAqEa+DOq5yvPwnwkPy6x6gySWjkh8b10LGonQsZXyzJx7grHoHMVFTPWERVtdw+\n"
            "rQ5zBQKBgQC0Iwx4eeQYx60OCZpioNEQ3QPaFgqoWYEexmcMlpgQ9ycdnHx3SkE8\n"
            "SlMokcPIEJDhdF3632kIAHOOJeA4Tmshf+ol/O2U2PDgbJZL6W6FJlT28sZVUU8j\n"
            "IjFmiAiW6IIEqkJxuR1diAjppEiMmSkjPavo7oQs0TZMMUkli1N9dw==\n"
            "-----END RSA PRIVATE KEY-----"
        )

    def setUp(self) -> None:
        """Setup mocked responses for the '/auth' endpoint."""
        load_responses_fixtures("auth.json")

    def test_base_url(self) -> None:
        """Test the base URL of the API."""
        url: str = self.client.url

        assert url == "https://api.transip.nl/v6"

    def test_authorization_header(self) -> None:
        """Test if the Authorization header is set correctly."""
        auth_header: str = self.client.headers["Authorization"]

        assert auth_header == "Bearer ACCESS_TOKEN"

    @responses.activate
    def test_private_key_authorization_header(self) -> None:
        """
        Test if TransIP instances initialized with a private key, results in
        the 'Authorization' header containing the access token returned by the
        mocked response.
        """
        client: TransIP = TransIP(login="testuser", private_key=self.privkey)
        auth_header: str = self.client.headers["Authorization"]

        # Assert a single request is made to the mocked TransIP API
        self.assertEqual(len(responses.calls), 1)
        # Assert the 'Authorization' header contains the access token returned
        # by the mocked response
        self.assertEqual(auth_header, "Bearer ACCESS_TOKEN")
