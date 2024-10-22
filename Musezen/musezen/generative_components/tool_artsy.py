import streamlit as st
import os

from musezen.external_integrations.ArtsyAPI import ArtsyAPI
from musezen.generative_components.agent_tools import AgentTool


SEARCH_GENE_DESCRIPTION = """
A 'gene' refers to a distinctive characteristic or attribute that defines an art object (e.g. 'Pop Art', 'Impressionism', 'Bright Colors'). This function returns information for the gene that matches the given query including:
- name: The official name of the gene.
- description: A detailed description of the gene.
- image_versions: List of available image formats for the gene (to put into template links in image).
- _links: A dictionary containing various related URLs including further API calls and public websites. e.g.:
    - thumbnail: Default image thumbnail.
    - image: Template link for different versions of the artist's main image.
"""


class SearchGene(AgentTool):
    def search_gene(query: str):
        """
        Search for a gene by query
        """
        st.write("Searching for art with characteristics of", query)
        client = ArtsyAPI(
            os.environ.get("ARTSY_CLIENT_ID"), os.environ.get("ARTSY_CLIENT_SECRET")
        )
        res = client.genes(query.lower().replace(" ", "-"))
        # st.write(res)
        st.write("Finished!")
        return res

    description = {
        "type": "function",
        "function": {
            "name": "search_gene",
            "description": SEARCH_GENE_DESCRIPTION,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The gene to search for (e.g., Pop Art, Impressionism, Bright Colors)",
                    },
                },
                "required": ["query"],
            },
        },
    }

    name = description["function"]["name"]

    executable = search_gene


SEARCH_ARTIST_DESCRIPTION = """
This function returns information for an artist that matches the given query including:
- 'type'/'og_type': The type of the entry, should be 'artist'.
- 'title': The name of the artist,.
- 'description': A detailed description of the artist, usualy None.
- '_links': A dictionary of web links related to the artist, with keys:
    - 'self': Contains a link to the artist's details with API endpoint.
    - 'permalink': Contains a link to the artist's page on Artsy.
    - 'thumbnail': Contains a link to an image thumbnail, normally be their painting, for the artist.
"""


class SearchArtist(AgentTool):
    def search_artist(query: str):
        """
        Search for a gene by query
        """
        st.write("Searching for artists:", query)
        client = ArtsyAPI(
            os.environ.get("ARTSY_CLIENT_ID"), os.environ.get("ARTSY_CLIENT_SECRET")
        )
        res = client.fetch_all_results(query=query, type_filter="artist")
        # st.write(res)
        st.write("Finished!")
        return res

    description = {
        "type": "function",
        "function": {
            "name": "search_artist",
            "description": SEARCH_ARTIST_DESCRIPTION,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Name of the artist to search for (e.g., Andy Warhol, Banksy)",
                    },
                },
                "required": ["query"],
            },
        },
    }

    name = description["function"]["name"]

    executable = search_artist


FETCH_APILINK_DESCRIPTION = """
Responses from the Artsy API requests usually contains various API links. This function fetches the response when given one of those links.
"""


class FetchAPILinks(AgentTool):
    def fetch_links(api_link: str):
        """
        Fetch the links for the Artsy API
        """
        st.write("Fetching responses from other further links...")
        client = ArtsyAPI(
            os.environ.get("ARTSY_CLIENT_ID"), os.environ.get("ARTSY_CLIENT_SECRET")
        )
        res = client.fetch_link(api_link)
        # st.write(res)
        st.write("Finished!")
        return res

    description = {
        "type": "function",
        "function": {
            "name": "fetch_links",
            "description": FETCH_APILINK_DESCRIPTION,
            "parameters": {
                "type": "object",
                "properties": {
                    "api_link": {
                        "type": "string",
                        "description": "The complete API link provided in responses from other API calls",
                    },
                },
                "required": ["api_link"],
            },
        },
    }

    name = description["function"]["name"]

    executable = fetch_links