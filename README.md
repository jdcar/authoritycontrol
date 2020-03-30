# authoritycontrol


This is a program with a user interface that helps with checking the linked personal names in Alma for accuracy. It displays the bib record (downloaded onto the computer) alongside the VIAF record (from viaf.org). 

Getting Started

You'll need to have a publishing profile setup in Alma so you can extract the bibliographic data with Linked Data.


1. Create a query in Alma Analytics of the records you want to check. My query includes: MMSID, Create Date, Modify Date, Author, Suppressed from Discovery. I filter by dates. I usually check 1 week at a time.
2. Create a set in Alma based on these records. 
3. Run the records in Publishing Profile. In the "Data Enrichement" tab, make sure "Linked Data Enrichment" is checked. Export as binary MARC files. Download the file to the computer. Change the file name in code to the location on the computer.
4. There are two options for each name: Submit or Next. Next just skips to the next heading. "Submit" prints useful information about the record into the console. When the program is done running, I save the console and edit Alma from the submitted results.
4. That should be it! 

The purpose of the program is to do two things: first, make it easy to go through personal names. Second, it elimates headings that meet certain criteria. If you want to include all personal names you will need to edit the code. This program eliminates headings that:

1. Have an 042 in the MARC
2. Have additional subfields, like $c, that help differentiate names
3. Names with more than two names. Includes: Doe, John. Excludes: Doe, John P.
I assume headings that include 1,2, and 3 to be correct.

If you have questions to message or email jamie.carlstone@northwestern.edu

