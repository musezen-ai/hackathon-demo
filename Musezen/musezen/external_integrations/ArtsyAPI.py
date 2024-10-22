import requests
import json
import time


class ArtsyAPI:
    def __init__(self, client_id, client_secret):
        self.base_url = "https://api.artsy.net/api"
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.token = self._get_token()
        self.session.headers.update({"X-Xapp-Token": self.token})

    def _get_token(self):
        """Retrieve the XAPP token needed for authentication."""
        url = f"{self.base_url}/tokens/xapp_token"
        params = {"client_id": self.client_id, "client_secret": self.client_secret}
        response = self.session.post(url, params=params)
        response.raise_for_status()  # Raise an error on bad status
        return response.json()["token"]

    def _make_request(self, endpoint, params=None):
        """General method to make authenticated requests to the API."""

        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_link(self, link):
        """Given a complete API link, fetch the data from the link."""
        response = self.session.get(link)
        response.raise_for_status()
        return response.json()

    def search(self, query, page_size=10, offset=0):
        """Search the Artsy database for any query term using optional type filtering."""
        params = {"q": query, "size": page_size, "offset": offset}
        return self._make_request("search", params=params)

    def fetch_all_results(
        self,
        query: str,
        type_filter: str | None = None,
        max_results: int = 10,
        max_pages: int = 5,
    ):
        """Fetch all results for a query, handling pagination, while maintaining the original response structure."""
        full_results = []
        page_size = 10
        offset = 0
        # Flag to capture the initial response structure
        initial = True
        final_response = {}

        while True:
            response = self.search(query, page_size, offset)

            if initial:
                # Capture the initial structure of the response
                final_response = response
                initial = False

            if "_embedded" in response and "results" in response["_embedded"]:
                # Filter results by type if type_filter is specified
                current_results = response["_embedded"]["results"]
                # Checking in loop since we have to throttle the requests anyways
                if type_filter:
                    current_results = [
                        r for r in current_results if r.get("type") == type_filter
                    ]
                full_results.extend(current_results)

            # If enough results are fetched or looked through first 5 pages, break the loop
            if (len(full_results) >= max_results) or (offset / page_size >= max_pages):
                break

            # Update offset based on response details
            if "next" in response.get("_links", {}):
                offset += page_size
            else:
                break

            # Throttle the requests to manage API rate limits
            time.sleep(0.2)

        # Update the final response with all accumulated results
        if "_embedded" in final_response:
            final_response["_embedded"]["results"] = full_results
        else:
            final_response["_embedded"] = {"results": full_results}

        return final_response

    def get_artists(self, **params):
        """
        An artist is generally one person, but can also be two people collaborating, a collective of people, or even a mysterious entity such as "Banksy".
        This function retrieves artists based on the provided parameters.

        Args:
            artwork_id (str): Retrieve artists for a given artwork.
            similar_to_artist_id (str): Return artists similar to a given artist.
            similarity_type (str): Similarity type, either default or contemporary.
            gene_id (str): Return a set of artists that represent a given gene.
            artworks (bool): Only return artists with artworks.
            published_artworks (bool): Only return artists with published artworks.
            partner_id (str): Return artists with artworks that belong to the partner.

        Returns:
            dict: A dictionary containing the response from the API, which is a paginated result with embedded artists.
        """
        return self._make_request("artists", params=params)

    def get_artist_by_id(self, artist_id):
        """Retrieve a specific artist by their ID."""
        return self._make_request(f"artists/{artist_id}")

    def genes(self, gene_id):
        """Retrieve information about a specific gene."""
        return self._make_request(f"genes/{gene_id}")
