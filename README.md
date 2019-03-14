
# EEBO-TCP Text Reuse

A set of notebooks for finding quotation and near quotation.

For a brief example of how matching works, see **matching_explained.ipynb**.

For the most part, these notebooks look for Bible quotation; however, as a bonus, there's a notebook for identifying reuse from the perspective of a single author or book.  And the development of an everything-to-everything process will continue in this repo.


# Inventory

This repo contains a bewildering variety of content.  It can be organized according the following scheme:


## Processes for Finding Biblical Quotation

**bible_to_verses.ipynb** -- Takes Bible XML from non-EEBO-TCP sources and transforms it into "bible pickles".  These pickles are by verse; for each verse, we keep track of its source, the raw tokens necessary to reconstruct a readable version of the verse, its non-stopword-etc lemma, the offsets of those lemma within the raw tokens, and "shingles" (which are lemma ngrams which starting and ending indexes to the lemma data).  NB: this notebook processes its inputs through morphadorner.

**bible_to_verses_from_TCP.ipynb** -- The same, but using morphadorned EEBO-TCP XMl as its input.

**multithreaded_shingle_generation.ipynb** -- Takes a folder of morphadorned EEBO-TCP files and generates a pickle for each file.  These files are similar to the bible pickles, except that we aren't dividing the text into verses.  This notebook uses the standard Python Queue and Thread modules to implement a process with multiple workers; with 6 workers, it processes EEBO-TCP (60,300 files) in about 4 hours on a recent, fairly generic Dell workstation.

**find_bible_quotation.ipynb** -- Like multithreaded_shingle_generation.ipynb, this is a multi-threaded process.  Using 6 workers, it will match 3 Bibles verse by verse against all of EEBO-TCP in about three hours (it's shockingly fast, but not fast enough to do everything-to-everything on a workstation).

The result is a folder of "bible matches", which contains one file for every EEBO-TCP file.  For each match between a bible verse and an EEBO-TCP file, we record the source file (i.e., which Bible), the verse, the text of the verse, the matching text from the Bible, the matching text from the EEBO-TCP file, the offset of the matching text within the verse (not especially useful), and the offset of the matching text with the EEBO-TCP file tokens.

**matching_functions.py** -- A collection of reusable functions for extracting data from EEBO-TCP files, converting that data to tokens, lemma, shingles, etc, and for matching two texts's pickles (e.g., a Bible verse and an EEBO-TCP file).  These functions do not know anything about Bible structure (that logic is in the Bible-specific notebooks); instead, they treat Bible verses like any other text. <span style="font-weight: bold; color:red">To-do: sprinkle in some doc strings.</span>

**metadata/** -- For the EEBO-TCP files. The metadata is CSV delimited by "|".

**xml_bible/** -- The source of the Bible data.  Files that start with A* are from EEBO TCP.  I'm really only using A10675.xml (an EEBO-TCP transcription of a 1562 edition of the Geneva Bible) and A97378.xml (an EEBO-TCP transcription of a 1668 edition of the King James Version).  KJV_OTA.xml is the King James from the Oxford Text Archive, and I do make use of it.

geneva/ contains the XML for a version of Geneva that I hoovered off the internet some time ago.  KJV_apocrypha/ was similarly sourced.  At present, I am not using these files.


## Processes for Evaluating Results

**basic_analysis_bible_quotation_A.ipynb** -- Basic counting, etc, mostly intended to examine the results of matching.  Are they reasonable?  Where are there gaps in my understanding of the data?  What are the broad outlines of the results?

**basic_analysis_bible_quotation_B.ipynb** -- Graphing the frequency of quotation for the most frequently quoted books and verses.  Are there trends worth noting?

**basic_one_book_of_bible.ipynb** -- A series of small bits which examine the Song of Solomon.  Do three versions (EEBPO_TCP Geneva, EEBO_TCP KJV, OTA KJV) align?  What else matches to one of those three transcriptions?


## General Purpose EEBO-to-EEBO Matching

**generalized_single_text_matching** -- A processing for matching any TCP file to all the other TCP files.  Useful for figuring out who quotes someone, or who he or she quotes.  *Perhaps obsolete once **do_everything.ipynb** is fully cooked.*

**do_everything.ipynb** -- A half-baked but promising method for finding text reuse across the whole corpus.  **Not complete**.


## Processes for Testing

These processes, especially test_matching_functions_part_1.ipynb, test_matching_functions_part_2.ipynb, and matching_explained.ipynb, are useful for understanding the process.

**testing_being_smarter_with_difflib.ipynb** -- Why am I not using Python's standard difflib SequenceMatcher?  This notebook explains the problem.

**test_matching_functions_part_1.ipynb** -- Part 1 of a set of tests for matching_functions.py, upon which so much rests.

**test_matching_functions_part_2.ipynb** -- Examples of using matching_functions.py to actually match test files. 

**matching_explained.ipynb** -- Walk through the process using a couple of toy files.

**test_by_matching_bible.ipynb** -- Matching my Geneva and the Oxford Text Archives KJV against the EEBO-TCP Geneva and KJV.

**check_bible_verses.ipynb** -- Print out a small portion of the data pickled by **bible_to_verses.ipynb** and **bible_to_verses_from_TCP.ipynb**.


