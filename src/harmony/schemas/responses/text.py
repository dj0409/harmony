'''
MIT License

Copyright (c) 2023 Ulster University (https://www.ulster.ac.uk).
Project: Harmony (https://harmonydata.ac.uk)
Maintainer: Thomas Wood (https://fastdatascience.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from typing import List, Any

import numpy as np
from pydantic import BaseModel, Field, RootModel

from harmony.schemas.catalogue_instrument import CatalogueInstrument
from harmony.schemas.requests.text import Instrument
from harmony.schemas.requests.text import Question

class InstrumentToInstrumentSimilarity(BaseModel):
    instrument_1_idx: int = Field(
        description="The index of the first instrument in the similarity pair in the list of instruments passed to Harmony (zero-indexed)")
    instrument_2_idx: int = Field(
        description="The index of the second instrument in the similarity pair in the list of instruments passed to Harmony (zero-indexed)")
    instrument_1_name: str = Field(description="The name of the first instrument in the similarity pai")
    instrument_2_name: str = Field(description="The name of the second instrument in the similarity pai")
    precision: float = Field(description="The precision score of the match between Instrument 1 and Instrument 2")
    recall: float = Field(description="The recall score of the match between Instrument 1 and Instrument 2")
    f1: float = Field(description="The F1 score of the match between Instrument 1 and Instrument 2")


class MatchResponse(BaseModel):
    instruments: List[Instrument] = Field(description="A list of instruments")
    questions: List[Question] = Field(
        description="The questions which were matched, in an order matching the order of the matrix"
    )
    matches: List[List] = Field(description="Matrix of cosine similarity matches")
    query_similarity: List = Field(
        None, description="Similarity metric between query string and items"
    )
    closest_catalogue_instrument_matches: List[CatalogueInstrument] = Field(
        default=[],
        description="The closest catalogue instrument matches in the catalogue for all the instruments, "
                    "the first index contains the best match etc."
    )
    instrument_to_instrument_similarities: List[InstrumentToInstrumentSimilarity] = Field(
        None, description="A list of similarity values (precision, recall, F1) between instruments"
    )


class SearchInstrumentsResponse(BaseModel):
    instruments: List[Instrument] = Field(description="A list of instruments")


class InstrumentList(RootModel):
    root: List[Instrument]


class CacheResponse(BaseModel):
    instruments: List[Instrument] = Field(description="A list of instruments")
    vectors: List[dict] = Field(description="A list of vectors")



# For use internally in the Python library but *not* the API because the NDarrays don't serialise
class HarmonyMatchResponse(BaseModel):
    questions: List[Question] = Field(
        description="The questions which were matched, in an order matching the order of the matrix"
    )
    similarity_with_polarity: Any = Field(description="Matrix of cosine similarity matches")
    query_similarity: Any = Field(
        None, description="Similarity metric between query string and items"
    )
    new_vectors_dict: dict = Field(
        None, description="Vectors for the cache. These should be stored by the Harmony API to reduce unnecessary calls to the LLM"
    )
    instrument_to_instrument_similarities: List[InstrumentToInstrumentSimilarity] = Field(
        None, description="A list of similarity values (precision, recall, F1) between instruments"
    )
