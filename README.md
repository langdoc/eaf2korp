## ELAN to Korp pipeline

This is a preliminary script to convert ELAN files, as structured in [IKDP project](http://langdoc.github.io/IKDP), as well as in several other language documentation projects, into VRT file format used in Korp. An introduction to VRT format can be found from the Language Bank of Finland's [Korp documentation](https://www.kielipankki.fi/development/korp/corpus-input-format/).

Bringing the corpus into Korp so that it can be accessed easily by wider audience fits well into the goals of [IKDP-2](http://langdoc.github.io/IKDP-2) project, which focuses in application of language technology into Komi resources, with focus in spoken corpora.

The pipeline is built so that annotations are parsed from ELAN files using [pympi](https://github.com/dopefishh/pympi) package, and annotations are added with [uralicNLP](https://github.com/mikahama/uralicNLP) package. This should make the pipeline rather flexible, as the only variables that need to be changed are the transcription tier and the language.

## To-do

- Timecodes and speaker id's need to be read from ELAN file
- Metadata needs to be added in one form or another
- Other morphological tags, besides POS, need to be added into other column. This also needs some decisions of what all we want, and how ambiguity is handled on that level.
- The utterances could be restructured into sentences by following punctuation characters. This would make the content more readable in Korp.
- The utterances, or whatever units we deal with, need to be ordered somehow in Korp. The best order would probably be the start time.
