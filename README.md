# Almanac of X
Given a person, I'd like to create an almanac for them. This will start with Joscha Bach.

## TODO/Roadmap:
- Run the whisper transcription on all of the youtube videos
- Gather all of Joscha's papers, and place that into the larger text dump as well
- Figure out the prompt to make it summarize each of the individaul artifacts (Podcast episode, paper, etc) to get a shorter summary, balancing brevity with covering the main aspects we care about from each artifact.
- Generate an overall outline of the book using all of the artifact summaries inside one massive file, by using Anthropic 100k. This should give us a table of contents, and for for each section/chapter, it should generate:
  - A summary of what the chapter will be about
  - Subsections of the chapter
  - Rationale for why the chapter is important
  - A list of sources from the context dump that will be the most useful for actually writing this chapter, when we need to actually write the thing.
- Prompt to actually produce the chapter itself. This will probably take in the chapter summary, associated resources, and maybe the overall table of contents / summary of the other sections, and turn that into a general outline/sections that the chapter should have, followed by the chapter itself.
- Make a prompt that reads the entire book, and asks which portions would be good spots to place an image inside of. Then, we can generate this image with Stable Diffusion.
- Package it into a book :)