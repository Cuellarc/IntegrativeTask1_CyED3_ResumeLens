# Literature Review

This review collects the main references behind the design of ResumeLens. For each formal model used in the project, it states what the literature says and how that supports the design decisions. The decisions are summarized in a table at the end.

## 1. Scope of the review

The review is a focused, non-systematic search. Its purpose is to ground the four stages of the system (regular expressions, finite-state transducers, finite automata and context-free grammars) and to place the project among résumé-processing work. Each reference was located through its bibliographic record (ACL Anthology, publisher or DOI). Some of the original texts are behind a paywall, so the summaries in this document follow the abstracts and bibliographic records.

## 2. Résumé information extraction

**Yu, Guan and Zhou (2005)** propose a *cascaded hybrid model* for extracting information from résumés. In a first pass, the résumé is segmented into consecutive blocks labeled with an information type (for example education or personal information). In a second pass, details such as the name or the address are extracted only inside the relevant blocks. The authors report a better F-score than flat models that ignore the hierarchical structure of résumés. ResumeLens follows the same idea on a smaller scale: the extraction expressions are anchored to labeled sections and to the shape of each line (`Location:`, `Summary:`, `role - organization (N years)`), so the same expression is not asked to work on the whole text.

**Chiticariu, Li and Reiss (2013)** study the gap between academia and industry in information extraction. They make the case for rule-based information extraction to industry practitioners and set a research agenda for improving rule-based systems. This supports the decision to use regular expressions in Stage 1: rules are a legitimate approach to extraction, and with them every extracted string can be traced back to the expression that produced it, which is also what the assignment asks us to document.

**Khaouja, Kassou and Ghogho (2021)** survey 108 articles on skill identification in job advertisements. They classify the work by skill bases, types of skills, identification methods, sector and granularity. Two of the dimensions of their classification frame choices that ResumeLens also had to make: the *skill base* (the vocabulary of skills that can be detected) and the *identification method*. In ResumeLens, the vocabulary is the catalog of the 41 qualifications used by the four profiles, and the method is rule-based. Because the same skill can be written in several ways, the project separates detecting a skill (Stage 1) from deciding which canonical qualification it is (Stage 2).

**Skill taxonomies.** The European classification **ESCO** (European Skills, Competences, Qualifications and Occupations) is a multilingual standard terminology that links skills and competences with occupations. It is an example of how a large-scale system manages a controlled vocabulary of skills, with terms available in each of its languages. The canonical names of our catalog (`NODE_JS`, `SCIKIT_LEARN`) and their lists of spellings play a similar role at a much smaller scale.

## 3. Regular expressions and finite automata

**Thompson (1968)** describes a search algorithm that compiles a regular expression into a machine that scans text and signals each match. It is the origin of the connection between regular expressions and nondeterministic finite automata used by most pattern-search tools. **Hopcroft, Motwani and Ullman** (*Introduction to Automata Theory, Languages, and Computation*) is the standard reference for the definitions that the project uses: regular expressions, DFAs, NFAs with and without ε-transitions and the equivalence among them. It is also the source of most of the algorithms implemented in the library `pyformlang`.

In ResumeLens, regular expressions describe the patterns of Stage 1. A finite automaton in Stage 3 recognizes the sequences of normalized qualifications. The automaton of each profile is a deterministic automaton, because the input has at most one qualification per category and the order of the categories is fixed.

## 4. Finite-state transducers for normalization

**Kaplan and Kay (1994)** show that phonological rewrite rules can be modeled as regular relations and implemented as finite-state transducers. This is the foundation for treating the rewriting of one spelling into another as a finite-state process. **Mohri (1997)** reviews finite-state transducers in language and speech processing: sequential transducers, their characterization theorems and algorithms such as determinization and minimization. The paper also explains why these machines are efficient to run, which is relevant when the same transducers are applied to every skill of every résumé.

**Sproat et al. (2001)** study the normalization of *non-standard words*, which are tokens that are not ordinary dictionary words, such as abbreviations, acronyms, mixed-case words, numbers, URLs and e-mail addresses, and which must be converted to a standard form. Our task has the same shape: `JS`, `Javascript` and `java script` are non-standard spellings that must become `JAVASCRIPT`.

In ResumeLens, each canonical qualification has one transducer with one path per spelling. The transducer reads the characters of the spelling and writes the canonical name on the last transition. The formal definition appears in [formalization_extraction_normalization.md](formalization_extraction_normalization.md).

## 5. Context-free grammars and domain-specific languages

**Chomsky (1956)** introduced the classification of grammars that later became the Chomsky hierarchy. It places regular languages and context-free languages at different levels. This explains why the project uses each model where it fits: regular expressions and automata for flat patterns, and a context-free grammar for the candidate profile, which has nested blocks (contact, experience, highlights, classification) that a regular expression cannot describe in general.

**Dejanović, Vaderna, Milosavljević and Vuković (2017)** present **textX**, a meta-language and Python tool for building domain-specific languages. From one grammar description, textX builds a parser and a meta-model at run time, and the parsing result is a Python object graph. textX is built on the Arpeggio parser, which is based on parsing expression grammars (PEG). A PEG uses ordered choice, so it is not identical to a context-free grammar, although the DSL of ResumeLens (blocks, lists and optional fields) can also be written as a context-free grammar. The EBNF documentation of the DSL describes the language in context-free terms.

## 6. Tools

**Romero (2021)** presents `pyformlang`, a pure-Python library for formal-language manipulation designed for teaching, with implementations of regular expressions, finite automata, finite-state transducers and context-free grammars. Its documentation states that most of its algorithms follow Hopcroft, Motwani and Ullman. The project uses it for Stage 2 (transducers) and Stage 3 (automata).

## 7. Responsible use of automated screening

**Raghavan, Barocas, Kleinberg and Levy (2020)** analyze vendors of algorithmic hiring tools and what they disclose about how their systems are built, validated and examined for bias, from both technical and legal perspectives. Their work shows that screening tools can have effects that are hard to see from the outside. ResumeLens takes a conservative position on this: it does not rank candidates or make hiring decisions. It only reports whether the qualifications explicitly written in a résumé satisfy a formally defined pattern, and every result can be traced back to a rule, a transducer path or an automaton transition.

## 8. How the literature supports the design decisions

| Design decision | Supporting references |
|---|---|
| Extract with regular expressions anchored to labeled sections and line shapes | Yu et al. (2005), Chiticariu et al. (2013) |
| Keep a normalization stage separate from extraction | Khaouja et al. (2021), Sproat et al. (2001), ESCO |
| Model spelling variants as finite-state transducers | Kaplan and Kay (1994), Mohri (1997) |
| One transducer per canonical qualification, with one path per spelling | Kaplan and Kay (1994), Hopcroft et al. |
| Recognize profile patterns with deterministic finite automata over the sorted sequence | Thompson (1968), Hopcroft et al. |
| Describe the candidate profile with a context-free grammar implemented in textX | Chomsky (1956), Dejanović et al. (2017) |
| Use `pyformlang` for transducers and automata | Romero (2021) |
| Do not rank candidates or decide; make every result traceable | Raghavan et al. (2020), Chiticariu et al. (2013) |

## 9. Limitations that the literature points out

- Rule-based extraction depends on how the résumé is written. Learned models, such as the one of Yu et al. (2005), can handle more variety, at the cost of data and transparency.
- A fixed catalog of spellings only normalizes the spellings it contains. Taxonomies like ESCO reach much wider coverage with managed vocabularies.
- A formal pattern checks explicit text only. It says nothing about the quality of the experience, and the bias questions raised by Raghavan et al. (2020) apply to any use of its output in a real hiring process.

## References

1. Chiticariu, L., Li, Y., and Reiss, F. R. (2013). Rule-Based Information Extraction is Dead! Long Live Rule-Based Information Extraction Systems! *Proceedings of EMNLP 2013*, pp. 827-832. https://aclanthology.org/D13-1079/
2. Chomsky, N. (1956). Three models for the description of language. *IRE Transactions on Information Theory*, IT-2(3), 113-124. https://doi.org/10.1109/TIT.1956.1056813
3. Dejanović, I., Vaderna, R., Milosavljević, G., and Vuković, Ž. (2017). TextX: A Python tool for Domain-Specific Languages implementation. *Knowledge-Based Systems*, 115, 1-4. https://doi.org/10.1016/j.knosys.2016.10.023
4. European Commission. ESCO: European Skills, Competences, Qualifications and Occupations. https://esco.ec.europa.eu/en/classification
5. Hopcroft, J. E., Motwani, R., and Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson/Addison-Wesley.
6. Kaplan, R. M., and Kay, M. (1994). Regular Models of Phonological Rule Systems. *Computational Linguistics*, 20(3), 331-378. https://aclanthology.org/J94-3001/
7. Khaouja, I., Kassou, I., and Ghogho, M. (2021). A Survey on Skill Identification from Online Job Ads. *IEEE Access*, 9, 118134-118153. https://doi.org/10.1109/ACCESS.2021.3106120
8. Mohri, M. (1997). Finite-State Transducers in Language and Speech Processing. *Computational Linguistics*, 23(2), 269-311. https://aclanthology.org/J97-2003/
9. Raghavan, M., Barocas, S., Kleinberg, J., and Levy, K. (2020). Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices. *Proceedings of ACM FAT\* 2020*. https://arxiv.org/abs/1906.09208
10. Romero, J. (2021). Pyformlang: An Educational Library for Formal Language Manipulation. *Proceedings of the 52nd ACM Technical Symposium on Computer Science Education (SIGCSE 2021)*, pp. 576-582. https://doi.org/10.1145/3408877.3432464
11. Sproat, R., Black, A. W., Chen, S., Kumar, S., Ostendorf, M., and Richards, C. (2001). Normalization of non-standard words. *Computer Speech & Language*, 15(3), 287-333. https://doi.org/10.1006/csla.2001.0169
12. Thompson, K. (1968). Programming Techniques: Regular expression search algorithm. *Communications of the ACM*, 11(6), 419-422. https://doi.org/10.1145/363347.363387
