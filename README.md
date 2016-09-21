# German/English Parallel Shell Noun Corpus

German/English parallel text from the [Europarl Corpus][europarl] with manually annotated shell noun complexes.

Annotations contain a series of noncontiguous turns (`turn`) from the Europarl corpus, grouped according to plenary session (`europarl_chunk`). The turns are presented in English/German pairs, with the language of a particular turn marked both in `turn_id` and in the `lang` attribute. The pairs were presented to annotators in random order, either German first or English first, in order to minimize bias towards one language or the other, and this is the order they occur in here as well.

The following excerpt shows how the data is organized:
```xml
<europarl_chunk source="../../ep-02-03-11.txt">
  <turn turn_id="t_02-03-11_12/en" lang="en">
    <alignUnit al_id="a_02-03-11_12/en.1">
      <sent sent_id="s_1">
        <tok mate_lemma="mr" mate_morph="_" mate_pos="NNP" id="t_1" mate_mother="t_2" mate_rel="NMOD">Mr</tok>
```

After the corpus base data there are two elements containing the actual shell noun–related data, `shellnouns` and `content_phrase`.

Each `shellnoun` element contains the following attributes:

`align_unit`
	: Identifier which all elements aligned to one another will share.
	
`content`
	: Either `given` (content is marked), `external` (content is
	probably present, but not in this turn), or, in rare cases
	`unclear` (unclear whether marked phrase is part of shell noun
	complex).
	
`content_phrases`
	: Reference to `id` of `content_phrase` element containing content
    of this shell noun instance.
    
`id`
	: Identifier for this shell noun instance.
	
`span`

	: Reference to token span corresponding to this shell noun instance.
	
`value`
	: Either `true` (this is a shell noun), `false` (not a shell
    noun), `undefined` (not annotated), or `unclear` (not clear
    whether this is a shell noun instance or not).
	
	
Each `content_phrase` element has the following attributes:

`align_unit`
	: As above.
	
`id`
	: Identifier for this content phrase instance.
	
`nominal`
	: If `true`, then this instance is nominal; if `false`, then sentential.
	
`span`
	: Reference to tokens. (See above.)



[europarl]: http://www.statmt.org/europarl/ "Europarl Parallel Corpus"
