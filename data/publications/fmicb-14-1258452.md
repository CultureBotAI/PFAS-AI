# fmicb-14-1258452

**Source PDF**: fmicb-14-1258452.pdf

---

## Page 1

Frontiers in Microbiology
01
frontiersin.org
Metabolism-linked methylotaxis 
sensors responsible for plant 
colonization in Methylobacterium 
aquaticum strain 22A
Akio Tani 1*, Sachiko Masuda 1,2, Yoshiko Fujitani 1, Toshiki Iga 1, 
Yuuki Haruna 1, Shiho Kikuchi 1, Wang Shuaile 1, Haoxin Lv 1, 
Shiori Katayama 3, Hiroya Yurimoto 3, Yasuyoshi Sakai 3 and 
Junichi Kato 4
1 Institute of Plant Science and Resources, Okayama University, Kurashiki, Japan, 2 Japan Science and 
Technology Agency, Advanced Low Carbon Technology Research and Development Program (JST 
ALCA), Kawaguchi, Japan, 3 Graduate School of Agriculture, Kyoto University, Kyoto, Japan, 4 Graduate 
School of Integrated Sciences for Life, Hiroshima University, Higashihiroshima, Japan
Motile bacteria take a competitive advantage in colonization of plant surfaces 
to establish beneficial associations that eventually support plant health. Plant 
exudates serve not only as primary growth substrates for bacteria but also as 
bacterial chemotaxis attractants. A number of plant-derived compounds and 
corresponding chemotaxis sensors have been documented, however, the 
sensors for methanol, one of the major volatile compounds released by plants, 
have not been identified. Methylobacterium species are ubiquitous plant surfacesymbiotic, methylotrophic bacteria. A plant-growth promoting bacterium, M. 
aquaticum strain 22A exhibits chemotaxis toward methanol (methylotaxis). Its 
genome encodes 52 methyl-accepting chemotaxis proteins (MCPs), among 
which we identified three MCPs (methylotaxis proteins, MtpA, MtpB, and MtpC) 
responsible for methylotaxis. The triple gene mutant of the MCPs exhibited no 
methylotaxis, slower gathering to plant tissues, and less efficient colonization 
on plants than the wild type, suggesting that the methylotaxis mediates initiation 
of plant-Methylobacterium symbiosis and engages in proliferation on plants. To 
examine how these MCPs are operating methylotaxis, we  generated multiple 
gene knockouts of the MCPs, and Ca2+-dependent MxaFI and lanthanide (Ln3+)-
dependent XoxF methanol dehydrogenases (MDHs), whose expression is regulated 
by the presence of Ln3+. MtpA was found to be a cytosolic sensor that conducts 
formaldehyde taxis (formtaxis), as well as methylotaxis when MDHs generate 
formaldehyde. MtpB contained a dCache domain and exhibited differential 
cellular localization in response to La3+. MtpB expression was induced by La3+, and 
its activity required XoxF1. MtpC exhibited typical cell pole localization, required 
MxaFI activity, and was regulated under MxbDM that is also required for MxaF 
expression. Strain 22A methylotaxis is realized by three independent MCPs, two 
of which monitor methanol oxidation by Ln3+-regulated MDHs, and one of which 
monitors the common methanol oxidation product, formaldehyde. We propose 
that methanol metabolism-linked chemotaxis is the key factor for the efficient 
colonization of Methylobacterium on plants.
KEYWORDS
methanol, formaldehyde, Methylobacterium species, chemotaxis, methyl-accepting 
chemotaxis protein
OPEN ACCESS
EDITED BY
Christopher Peter Chanway, 
University of British Columbia, Canada
REVIEWED BY
Santosh Kumar, 
University of Wisconsin-Madison, United States 
Song Yang, 
Qingdao Agricultural University, China
*CORRESPONDENCE
Akio Tani 
 atani@okayama-u.ac.jp
RECEIVED 14 July 2023
ACCEPTED 02 October 2023
PUBLISHED 13 October 2023
CITATION
Tani A, Masuda S, Fujitani Y, Iga T, Haruna Y, 
Kikuchi S, Shuaile W, Lv H, Katayama S, 
Yurimoto H, Sakai Y and Kato J (2023) 
Metabolism-linked methylotaxis sensors 
responsible for plant colonization in 
Methylobacterium aquaticum strain 22A.
Front. Microbiol. 14:1258452.
doi: 10.3389/fmicb.2023.1258452
COPYRIGHT
© 2023 Tani, Masuda, Fujitani, Iga, Haruna, 
Kikuchi, Shuaile, Lv, Katayama, Yurimoto, Sakai 
and Kato. This is an open-access article 
distributed under the terms of the Creative 
Commons Attribution License (CC BY). The 
use, distribution or reproduction in other 
forums is permitted, provided the original 
author(s) and the copyright owner(s) are 
credited and that the original publication in this 
journal is cited, in accordance with accepted 
academic practice. No use, distribution or 
reproduction is permitted which does not 
comply with these terms.
TYPE  Original Research
PUBLISHED  13 October 2023
DOI  10.3389/fmicb.2023.1258452

## Page 2

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
02
frontiersin.org
Introduction
Microbial plant colonizers recognize the existence of plants by 
sensing the chemicals released by plants to establish their symbiotic 
or pathogenic relationships (Scharf et al., 2016). Most motile bacteria 
have an array of sensors called methyl-accepting chemotaxis receptors 
(MCPs). MCPs and the cooperating Che system that transmits the 
signals from MCPs to the flagellar motor regulate the direction of 
flagellar rotation and enable attractant-directed swimming, defined as 
chemotaxis (Karmakar, 2021). The chemotaxis mechanism has been 
extensively studied using Escherichia coli as a model organism. The 
E. coli genome encodes five MCP genes, whose detailed function and 
their ligands have been studied well (Sourjik and Armitage, 2010). In 
contrast, plant-colonizing bacteria possess huge numbers of MCPs. 
For example, Rhizobium species have 15 to 30 MCPs, Agrobacterium 
species have 20 to 40 MCPs, and Bradyrhizobium species have 30 to 
60 MCPs (Scharf et al., 2016). These receptors typically contain an 
N-terminal ligand-binding region and a C-terminal signaling region 
containing a methyl-accepting domain. The ligand-binding domains 
of the large majority (~88%) of bacterial MCPs have not been 
annotated (Lacal et al., 2010).
Methylobacterium species are ubiquitous methylotrophic 
colonizers on plant aerial surfaces (phyllosphere), and they can occupy 
10 to 20% of total culturable bacteria on plant surfaces (Vorholt, 
2012). Methanol released by plants as a byproduct of pectin 
degradation (Fall and Benson, 1996) offers a niche for methylotrophic 
bacteria. Plant-associated methylotrophic bacteria are also capable of 
synthesizing phytohormones that can affect plant growth, resulting in 
plant growth promotion (Dourado et  al., 2015). Thus, 
Methylobacterium species are recognized as mutual symbionts 
for plants.
Methylobacterium species oxidize methanol mainly using two 
different methanol dehydrogenases (MDHs), MxaFI and XoxF. The 
former is a calcium (Ca2+)-dependent enzyme, whereas the latter was 
found to be a lanthanide (Ln3+)-dependent enzyme (Anderson et al., 
1990; Hibi et al., 2011; Nakagawa et al., 2012; Keltjens et al., 2014). 
Another Ln3+-dependent alcohol dehydrogenase, ExaF, was found in 
Methylorubrum extorquens strain AM1 (Good et  al., 2016) and 
Methylobacterium aquaticum strain 22A (Yanpirat et  al., 2020). 
Recognition and transport of Ln3+, Ln3+-dependent regulation of 
methylotrophy genes, and catalytic and regulatory activity of XoxF are 
currently emerging fields of study on methylotrophic bacteria 
(Skovran et al., 2011; Vu et al., 2016; Ochsner et al., 2019; RoszczenkoJasińska et al., 2020). Though Lns are included in “rare earth metals,” 
the concentration of Ln3+ in soils is not low and is almost equivalent 
to those of copper, cobalt, and zinc (Kamenopoulos et al., 2016). XoxF 
is more widespread in methylotrophic bacteria than MxaF and is 
believed to be closer to an ancient form of MDHs (Chistoserdova, 
2019; Skovran et al., 2019). Thus, Ln3+ has a pivotal regulatory role in 
the methylotrophy and physiology of methylotrophic bacteria (Tani 
et al., 2021).
Methylobacterium aquaticum strain 22A is an isolate from a 
hydroponic culture of a moss, Racomitrium japonicum, and is also a 
potent plant growth promoter (Tani et al., 2012). The strain has the 
MDHs described above (MxaFI and XoxF1) as well as ExaF (Tani 
et al., 2015; Masuda et al., 2018; Yanpirat et al., 2020). XoxF1 and ExaF 
are induced by Ln3+, whereas MxaF is induced in the absence of Ln3+. 
For formaldehyde oxidation, the strain employs two different 
pathways, the H4MPT pathway and the GSH pathway (Yanpirat 
et al., 2020).
The 22A genome encodes as many as 52 MCPs. As reported 
previously, we found that some bacteria including Methylobacterium 
species exhibit chemotaxis toward methanol (Tola et al., 2019). In this 
study, we revealed that strain 22A has three MCPs each responsible 
for chemotaxis towards methanol and its metabolite formaldehyde 
(here we  define methylotaxis and formtaxis, respectively), the 
methylotaxis is realized by the coordination of MCPs with the 
methanol metabolism that is regulated by Ln3+, and the methylotaxis 
has a critical role in locating plants.
Results
Identification of three MCPs involved in 
methylotaxis
A microscopy-aided capillary-plug assay was employed to assess 
chemotaxis activity. Strain 22A methylotaxis was inducible by 
methanol (Supplementary Figure S1). Strain 22A cells were incubated 
in HEPES buffer (20 mM, pH 7.0) at 20°C for 2 h after overnight 
cultivation on methanol (as optimized in Supplementary 
Figures S1B,C). Strain 22A exhibited taxis toward DL-malate, 
DL-glycerate, and L-glutamate (Supplementary Figure S1D). The 
amino acid sequences of 52 MCP genes encoded in the strain 22A 
genome conserve a common MCP signal domain at their C-terminus 
in most cases, and other different domains, such as dCache, 4HB_
MCP_1, and HAMP domains (Supplementary Figure S2). 
We generated single-gene knockout mutants for 15 genes that are 
induced by methanol in the transcriptome data of strain 22A (Masuda 
et al., 2018), but none of the mutants lost methylotaxis completely 
(Supplementary Figure S3). Because mtpA knockout strain (maq22A_
c14925, ΔmtpA) exhibited significantly weaker methylotaxis than the 
wild type, we hypothesized that strain 22A has multiple methylotaxis 
MCPs. Then, we generated multi-gene knockouts based on ΔmtpA 
mutant. The additional knockouts of mtpB (maq22A_1p32440) and 
mtpC (maq22A_c15300) that also showed weaker methylotaxis in the 
screening, resulted in a complete loss of methylotaxis. Hereafter 
we call ΔmtpAΔmtpBΔmtpC mutant the TM (triple gene mutant).
The TM grown on methanol in the presence and absence of LaCl3 
did not exhibit any methylotaxis (Figure 1A) but retained chemotaxis 
toward yeast extract (2%) used as a mixture of amino acids. These 
results suggested that the mutant is not impaired in its chemotaxis 
machinery but only in attractant recognition and that the taxis 
response of La3+ is specific to methanol.
In MtpA amino acid sequence we detected only an MCP signaling 
domain (Figure 1B) involved in its dimerization and interaction with 
CheA protein and the adaptor protein CheW. The absence of the 
transmembrane region suggested that MtpA operates in the 
cytoplasm. MtpB contains a putative signal peptide, dCache_1 
domain, a transmembrane domain, and a HAMP domain. The 
dCache_1 is the predominant sensor domain that recognizes wide 
variety of compounds including proteinogenic amino acids, 
polyamines, quaternary amines, purines, organic acids, sugars, 
quorum sensing signals, or inorganic ions (Matilla et al., 2021). The 
HAMP domain transmits the outside signal into the cytosol 
(Parkinson, 2010). MtpC contains a signal peptide, a transmembrane

## Page 3

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
03
frontiersin.org
region, and a HAMP domain, exhibiting a typical structure of general 
MCPs. The predicted periplasmic domain has no sign for any known 
domains. Thus, we concluded that MtpA has atypical topology IV 
(cytosolic receptor), and MtpB and MtpC have typical topology I with 
an extracellular ligand binding domain, according to the classification 
by Lacal et al. (2010).
The single-gene knockouts of three MCPs exhibited different 
intensities of methylotaxis (Figure 1C). Deletion of mtpA resulted in 
a significant decrease in methylotaxis activity, suggesting its major 
contribution to cellular methylotaxis. Whereas methylotaxis of 
∆mtpA and ∆mtpC mutants was not affected by the presence of LaCl3, 
ΔmtpB mutant exhibited weaker methylotaxis when it is grown on 
methanol in the presence of LaCl3 (hereafter called the MeOH+La 
condition) than when it is grown on methanol in the absence of LaCl3 
(MeOH-La condition), suggesting that MtpB contributes to 
methylotaxis more in the presence of La3+. Indeed, mtpB expression is 
approximately twofold increased by La3+ (Supplementary Figure S3).
Then we examined the sensitivity and Ln-dependency of the 
methylotaxis of the double gene knockouts (Figure 1D), and found 
that MtpA is a relatively sensitive sensor, MtpB is a relatively lesssensitive sensor operating in the presence of La3+, and MtpC is a 
relatively less-sensitive sensor operating in the absence of La3+. These 
FIGURE 1
(A) Methylotaxis and chemotaxis toward the yeast extract of strain 22A wild type and TM grown on methanol in the absence and presence of LaCl3. 
The data are presented as the mean  ±  standard deviation (SD; n = 3). Blue (circle), wild type; red (square), TM; closed symbols, the absence of LaCl3; 
open symbols, the presence of LaCl3. The data are presented as the mean ± SD (n = 3). (B) Schematic diagram of methylotaxis MCPs structures. The 
conserved motifs, transmembrane domain, and signal peptide in the methylotaxis MCPs were analyzed by GenomeNet MOTIF Search (https://www.
genome.jp/tools/motif/), TMHMM Server v 2.0 (http://www.cbs.dtu.dk/services/TMHMM/), and SignalP (http://www.cbs.dtu.dk/services/SignalP/), 
respectively. The motif search was carried out with the Pfam database, and a cut-off score e-value of 0.001. The transmembrane domain was regarded 
as the amino acids of score  >  0.6. Motifs: MCP signal, PF00015 Methyl-accepting chemotaxis protein (MCP) signaling domain; HAMP, PF00672 HAMP 
domain; and dCache_1, PF02743 Cache domain (double cache; CAlcium channels and CHEmotaxis receptors). Arrows indicate putative signal peptide 
cleavage sites. Numbers indicate amino acid positions. Bar, 100 amino acids. (C) Methylotaxis rate of strain 22A wild type (WT) and single methylotaxis 
MCP gene knockouts, grown on methanol in the absence/presence of LaCl3. The data were analyzed with the Student’s t-test and are shown as the 
mean rate  ± standard deviation (SD; n  =  3). (D) Methylotaxis of strain 22A wild type (WT) and double MCP gene knockouts, grown on methanol in the 
absence/presence of LaCl3, toward varied concentrations of methanol. The data are shown as the mean rate ± SD (n = 3). (E) Cellular localization of 
GFP-tagged MCPs. The strain 22A wild type transformed with GFP-tagged MCP genes was grown on methanol in the presence/absence of LaCl3 for 
2  days and subjected to confocal microscopy. Bar, 10 μm.

## Page 4

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
04
frontiersin.org
data indicated that each MCP with different sensitivity operates 
independently, and their expression and activity depend on the 
availability of La3+.
The methylotaxis MCPs were expressed as green fluorescent 
protein (GFP)(C-terminal)-fusion proteins under the control of their 
promoters in strain 22A wild type, and their cellular localization was 
examined with confocal microscopy (Figure 1E). The promoter-less 
vector control did not exhibit any fluorescence. MtpA-GFP 
localization was observed in the cytoplasm, as predicted above. The 
MtpB-GFP signal was observed at the pole of the cells grown in the 
MeOH-La condition, whereas interestingly, it was observed at the cell 
periphery in the MeOH+La condition. The MtpC-GFP signal was 
observed at the cell pole. It is known that essentially all of the MCP 
molecules cluster together with CheA and CheW to form the 
chemotaxis sensory array at the cell pole (Briegel et al., 2009).
The methylotaxis MCP genes with their promoter region were 
PCR-amplified and cloned into pAT01 (Fujitani et  al., 2022) to 
generate pAT01-MtpA, -MtpB, and-MtpC. The methylotaxis of TM 
transformed with these plasmids was examined (Supplementary 
Figure S4). The TM carrying pAT01-MtpA showed comparable 
methylotaxis activity irrespective to the presence of LaCl3. The TM 
carrying pAT01-MtpB and-MtpC showed higher methylotaxis when 
grown in the presence and absence of LaCl3, respectively. These 
responses to La3+ were in line with the result obtained in 
Figure 1D. These gene complementation experiments indicated that 
the phenotype of the mutants was caused by the MCP gene deletion 
and not by polar effect.
The TM exhibited no growth defect on methanol, irrespective of 
the presence of La3+ (Supplementary Figure S5), suggesting that the 
methylotaxis MCPs are not involved in methanol metabolism and 
its regulation.
Methylotaxis engages in locating plants 
and phyllospheric growth
To examine whether methylotaxis is involved in locating plants, 
first, we quantified the methanol exuded by rice roots in hydroponic 
culture (Supplementary Figure S6). After 8 h of seedling 
transplantation, the methanol concentration in the medium reached 
a maximum (3.5 mM = 0.01% w/v) and then gradually decreased. The 
methanol exudation rate was calculated to be  approximately 
0.113 mmol (=3.6 mg)/g plant fresh weight/h.
The taxis toward Arabidopsis and rice roots was examined by 
counting the number of cells gathered and attached to the roots after 
soaking the roots in the cell suspensions (Figure 2A). The wild-type 
cells gathered to plant roots rapidly, but the TM exhibited less efficient 
gathering in the tested duration. These results suggested that the 
methanol and methylotaxis of strain 22A engage in locating the plants. 
The strain 22A wild-type cells gather at specific sites at the edge of 
Arabidopsis leaves, where they swim around actively (Figure 2B). 
These sites should be stomata or hydathodes, which are most possibly 
the sites releasing methanol.
To reveal the physiological role of methylotaxis in the 
phyllosphere, the ability of seed-inoculated strain 22A and TM to 
colonize plant leaves was compared. The cells were labeled with the 
fluorescent protein mVenus and inoculated on sterilized red perilla 
seeds that were cultivated aseptically. During cultivation, the cells 
washed off from the leaves were quantified by flow cytometry. 
Whereas the cell number of TM remained low during the course of 
experiment, at certain time points (e.g., at 55 and 96 days) the number 
of wild-type cells was significantly higher than that of TM cells 
(Figure 2C). These large fluctuations might be due to plasmid loss in 
the non-selective experimental setup and also to ununiform 
colonization pattern of the cells on individual plants and leaves. Leafimprinting also indicated that the wild type 22A colonized red perilla 
leaves more widely and densely than the TM (Figure 2D). These 
results suggested that methylotaxis contributes to efficient colonization 
in the phyllosphere.
Formtaxis as a metabolism-linked 
methylotaxis
Methylobacterium species oxidize methanol rapidly with MDHs, 
and the product formaldehyde is taken into the cytosol for further 
oxidation and assimilation. However, it is also released extracellularly 
(Masuda et al., 2018) from the periplasm where the oxidation by 
MDHs occurs. If strain 22A is chemotactic to formaldehyde, the 
methylotaxis observed above may include formtaxis. Strain 22A 
exhibited formtaxis irrespective of La3+ and the TM did not exhibit any 
formtaxis (Figure  3A). This result suggested that any of the 
methylotaxis MCP(s) is also involved in formtaxis, and no MCPs 
other than these three MCPs encoded in the genome are involved in 
formtaxis, as long as the strain is grown in the used conditions.
Next, we examined the formtaxis in double-gene knockouts of 
methylotaxis MCPs with varied concentrations of formaldehyde 
(Figure 3B). The wild type exhibited stronger formtaxis when grown 
in the MeOH-La condition than in the MeOH+La condition, and the 
best concentration of formaldehyde was 0.2%. ΔmtpBΔmtpC mutant 
exhibited strong formtaxis compared to the wild type, for the high 
concentration of formaldehyde (2%) only when it was grown in the 
MeOH-La condition. ΔmtpAΔmtpC mutant exhibited moderate 
formtaxis when grown in the MeOH-La condition, for 0.2% 
formaldehyde. ΔmtpAΔmtpB mutant exhibited almost no formtaxis 
at any tested concentrations of formaldehyde. Thus, MtpC is involved 
only in methylotaxis and not in formtaxis.
Strain 22A did not exhibit any taxis toward 2 and 0.2% formate 
that is also a metabolite in methylotrophic pathway (data not shown), 
although formate serves as a chemoattractant for a soil plant pathogen, 
Agrobacterium fabrum strain C58 (Wang et al., 2021).
The strain 22A genome encodes genes for the H4MPT pathway 
that plays a central role in formaldehyde oxidation, starting with the 
reaction catalyzed by the formaldehyde-activating enzyme (Fae). 
Strain 22A has two homologous fae genes (fae1 and fae2). Strain 22A 
(and many other Methylobacterium strains in the C1 clade, Alessa 
et al., 2021) have additional glutathione-dependent formaldehyde 
oxidation pathway (GSH pathway) genes composed of gfa 
(glutathione-dependent formaldehyde-activating enzyme), hgd 
(S-hydroxymethyl 
glutathione 
dehydrogenase), 
and 
fgh 
(S-formylglutathione hydrolase). The Δfae1Δfae2Δhgd mutant is 
completely defective in formaldehyde metabolism and unable to grow 
even on succinate in the presence of methanol, due to formaldehyde 
toxicity (Yanpirat et al., 2020). The mutant grown in the absence of 
methanol did not lose methylotaxis and formtaxis (Figure  3C), 
suggesting that methylotaxis and formtaxis do not require the

## Page 5

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
05
frontiersin.org
formaldehyde metabolic pathways. Whereas the chemotactic cells 
usually gather and swim around the capillary mouth in the assay, the 
mutant cells could no longer swim once gathered around the capillary, 
suggesting that they were toxified by formaldehyde (data not shown). 
The Δfae1Δfae2Δhgd mutant exhibited stronger formtaxis than the 
wild type in the presence of La3+, the possible reason for which is 
discussed below.
Examination of the relationships between 
MDHs and MCPs revealed that MtpA is 
responsible for formtaxis
To examine the involvement of MDHs in methylotaxis and 
formtaxis, we tested MDH gene knockouts of strain 22A grown on 
succinate plus methanol. XoxF1 is necessary for the expression of 
MxaF, therefore, ΔxoxF1 mutant cannot grow on methanol, 
irrespective of La3+. ΔmxaF mutant can grow on methanol only in the 
presence of La3+ due to intact XoxF1. ΔxoxF1Sup mutant is a 
suppression mutant derived from ΔxoxF1 mutant that carries a 
mutation in mxbD encoding a sensor kinase responsible for mxaF 
expression, and the mutant restored the mxaF-dependent growth on 
methanol without xoxF1 (Yanpirat et al., 2020).
ΔxoxF1 and ΔxoxF1ΔmxaF mutants did not exhibit any 
methylotaxis but retained formtaxis (Figure 4). ∆mxaF mutant grown 
in the presence of La3+ and ∆xoxF1Sup retained methylotaxis. Thus, 
either of the active MDHs is necessary for methylotaxis, and formtaxis 
does not necessitate active MDHs. Namely, there may be MCP(s) that 
recognize(s) formaldehyde.
To differentiate which of methanol and formaldehyde is 
recognized by each MCP, we generated double methylotaxis MCP 
gene knockouts in the background of a series of MDH gene 
knockouts (Figure 4). All mutants were motile under microscopic 
observation, and TM under ∆mxaF∆xoxF1 background exhibited 
wild-type level of taxis toward yeast extract (data not shown), 
supporting the idea that the defect in methylotaxis was not due to the 
loss of swimming motility.
The ΔmtpBΔmtpC knockout mutants under ΔxoxF1 and 
ΔmxaFΔxoxF1 backgrounds retained formtaxis irrespective of 
La3+, 
whereas 
they 
lost 
methylotaxis, 
suggesting 
that 
FIGURE 2
(A) Taxis of strain 22A wild type (WT) and TM for Arabidopsis and rice root. The taxis was evaluated as the CFUs attached to the plant root per fresh 
weight of the tissues. The data are presented as the mean  ±  standard deviation (n = 3) and analyzed with the Student’s t-test. (B) Gathering of strain 22A 
wild type cells to specific sites at the edge of young Arabidopsis leaf. Scales are shown in the pictures. (C) Quantification of mVenus-labeled strain 22A 
cells on the red perilla leaves. Cells of strains WT-mVenus and TM-mVenus were inoculated on red perilla seeds and the plants were cultivated. Fresh 
leaves were collected on the indicated days after sowing and mVenus-labeled cells were counted by flow cytometry. One to four leaves were sampled 
at each time point. Asterisks indicate p values less than 0.05 (Student’s t-test). (D) Fluorescence stereo-microscopic images of leaf-printed colonies of 
WT-mVenus and TM-mVenus. Fresh leaves collected 32, 56, and 112 days after sowing were impressed onto the methanol-agar plate, and colonies 
were observed by fluorescence stereo-microscopy. Bars indicate 2 mm.

## Page 6

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
06
frontiersin.org
MtpA-dependent methylotaxis depends on formaldehyde 
generation by MDHs, and MtpA-dependent formtaxis does not 
require MDHs. Therefore, MtpA is responsible for formtaxis. The 
relatively high formtaxis in ΔmtpBΔmtpC mutant under 
ΔmxaFΔxoxF1 background in the presence of La3+ might be due 
to formaldehyde generation by ExaF that is active for methanol as 
well as ethanol. Interestingly, the ΔmtpBΔmtpC mutant under 
ΔxoxF1Sup background exhibited high methylotaxis and 
formtaxis. ΔxoxF1Sup mutant constitutively and highly expresses 
mxaF. Therefore, formaldehyde generated by MxaF might 
promote the taxis.
The vector for the MtpA-GFP construct was introduced into the 
TM, 
and 
the 
transformant 
exhibited 
formtaxis 
(Supplementary Figure S7), suggesting that the cytosol-localized 
GFP-tagged MtpA (Figure 1E) is functional.
MtpB depends on MDH activity and La3+
The ΔmtpAΔmtpC mutants under any MDH knockouts lost 
methylotaxis and formtaxis in the absence of La3+ (Figure 4), partly 
because the expression of mtpB is low in the absence of 
La3+(Supplementary Figure S3). In the presence of La3+, the 
ΔmtpAΔmtpC mutant under ΔmxaF and ΔxoxF1Sup backgrounds 
retained low but significant levels of taxis, because either of the MDHs 
is operating in these mutants.
The strong formtaxis exhibited in Δfae1Δfae2Δhgd mutant in the 
presence of La3+ (Figure  3C) might be  due to the formaldehyde 
accumulation caused by the mutation and the participation of the 
MtpB activity sensing XoxF1-dependent formaldehyde oxidation.
Strain 22A grown on methanol also exhibited ethanol-taxis, and 
the assay with double MCP gene knockouts suggested that MtpB 
contributes most to the ethanol-taxis (Supplementary Figure S8A). 
TM exhibited weak activity in the absence of La3+, suggesting that 
strain 22A has other unidentified MCPs for ethanol-taxis that operate, 
especially in the absence of La3+. The methylotaxis activity was 
competitively lost in the presence of high concentrations of ethanol 
(Supplementary Figure S8B).
MtpC activity necessitates MxaF and is 
under the regulation of MxbDM
The ΔmtpAΔmtpB mutants exhibited almost no methylotaxis or 
formtaxis under backgrounds of ΔmxaF, ΔxoxF1, and ΔmxaFΔxoxF1, 
but exhibited strong taxis for both attractants under a ΔxoxF1Sup 
background (Figure 4), suggesting that the activity or expression of 
MtpC depends on MxaF. To examine whether the expression of MtpC 
depends on the expression of mxaF, we  measured the promoter 
activity of mtpC (PmtpC) in various MDH knockouts using a promoterreporter (luciferase) vector (Figure 5). The PmtpC activity was notably 
higher in ΔxoxF1Sup mutant, and negligible in ΔxoxF1 and 
ΔmxaFΔxoxF1 mutants. The PmtpC activity was not lost in ΔmxaF 
mutant, suggesting that the expression of mtpC is not dependent on 
the presence of mxaF. Therefore, we conclude that MtpC is dependent 
on MxaF activity but not on its expression. Namely, the ligand for 
MtpC is not methanol.
mxaF expression is dependent on the presence of xoxF1 and a 
two-component signaling system, MxbDM. The PmtpC activity was 
abolished almost completely in the ∆mxbD mutant, suggesting that 
mtpC expression is under regulation by mxbDM, which also 
regulates mxaF.
FIGURE 3
(A) Chemotaxis toward 0.2% formaldehyde (formtaxis) in strain 22A 
wild type (WT) and TM grown on methanol in the presence/absence 
of La3+. The data were analyzed with Student’s t-test and are shown 
as the mean rate  ±  standard deviation (SD; n  =  5). (B) Formtaxis rate 
of strain 22A wild type and double methylotaxis MCP gene 
knockouts, grown on methanol in the absence/presence of LaCl3, 
toward varied concentrations of formaldehyde. The data are shown 
as the mean rate  ±  SD (n  =  3). (C) Methylotaxis and formtaxis rates of 
the wild type and formaldehyde oxidation-deficient mutant 
(Δfae1Δfae2Δhgd). Both strains were grown on succinate in the 
presence/absence of La3+ and subjected to taxis assay. The data were 
analyzed with the Student’s t-test and only the significant p-value 
(p  <  0.05) is indicated. The data are shown as the mean rate  ±  SD 
(n  =  3).

## Page 7

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
07
frontiersin.org
Discussion
Chemotaxis is one of the bacterial survival strategies that enable 
the cells to reach nutrients, and also to establish symbiotic and 
associative relationships between hosts and microorganisms (AllardMassicotte et al., 2016; Scharf et al., 2016; Feng et al., 2019). Previously, 
we showed that environmental bacteria including Methylobacterium 
species exhibited methylotaxis (Tola et  al., 2019). However, its 
molecular mechanism and contribution to bacterial survival have 
remained elusive. In this study, we proved that a methylotrophic 
plant–growth promoting bacterium M. aquaticum strain 22A has as 
many as three MCPs for methylotaxis (Figure 1).
Strain 22A utilizes methylotaxis to locate the plant and to initiate 
symbiosis, and gathers in specific niches of natural openings, such as 
stomata and hydathodes (Figures 2A,B). The seed-inoculated TM 
exhibited less efficient colonization on perilla leaves than the wild type 
(Figures 2C,D). It is currently unknown whether this is a result of the 
fewer opportunities to reach favorable niches that eventually support 
bacterial cell proliferation or the cellular spontaneous migration from 
seeds to leaves on the plant surface or through internal tissues of the 
vascular system (Chi et al., 2005; Ji et al., 2010). Methylotaxis is one of 
the survival strategies that enable Methylobacterium cells to reach 
nutrients and to establish symbiosis with plants.
Although three MCPs are involved in the same cellular function 
of methylotaxis, they operate independently and have distinctly 
different characteristics in their secondary structures, induction 
response to La3+, sensitivity, and cellular localization. To add an 
evolutionary viewpoint to their function and conservation, 
we examined MCP genes in the genomes of 62 type strains of the 
genera (1,467 MCP genes in total, 23.3 genes per genome, 
Supplementary Table S1). The type strains of clade A and C with 
relatively larger genomic sizes contain relatively larger numbers of 
MCP genes (average: 34 genes). We  also tested the methylotaxis 
activity of the type strains grown in the MeOH+La condition that 
supports the growth of all type strains. Twenty-six strains among the 
tested 60 type strains exhibited swimming motility, and all of them 
exhibited methylotaxis with different intensities. The methylotaxis 
MCP genes found in this study were not necessarily conserved in 
these strains, suggesting that another type of methylotaxis MCP exists.
MtpA was found to function in the cytosol (Figure  1E; 
Supplementary Figure S7) and is primarily responsible for formtaxis 
(Figure 3B), but also engages in methylotaxis when MDH is functional 
(Figure 4). MtpA is considered to be a sensor for methylotaxis that 
navigates the cells to the place where more formaldehyde is produced. 
Although formaldehyde can also be detected in plants (Blunden et al., 
1998), considering the difference in sensitivity of methylotaxis and 
formtaxis (Figures 1D, 3B), abundant methanol emission from plants 
(Supplementary Figure S6), and ubiquity of functional MDHs in 
Methylobacterium species, methylotaxis would first be prioritized to 
locate plants in nature. It is reported that E. coli cells are supposed to 
secrete serine upon being attracted by aspartic acid, and serine is used 
as a signaling molecule to attract other cells (Long et al., 2017). The 
formaldehyde secreted by the methanol-oxidizing cells may serve as a 
secondary signal to gather other Methylobacterium cells and to 
enhance the colonization of the species. Although MtpA is conserved 
in clade C members (Supplementary Table S1) in which the GSH 
pathway is also conserved (Alessa et al., 2021), the formtaxis did not 
necessitate the formaldehyde metabolism pathways. Thus, it is unlikely 
that a metabolic intermediate (such as S-formylglutathione, H4MPT, 
etc.) in the pathways is the ligand for MtpA. The clade C members are 
considered to be  evolutionary ancestors that may prefer soil, 
rhizosphere, or aquatic environments to the phyllosphere (Leducq 
et al., 2022). It is interesting to hypothesize that MtpA-dependent 
formtaxis may contribute to colonizing a niche by convening 
colleagues in such environments. There is no hint for ligand based on 
MtpA structural information. It is reported that about one-quarter of 
FIGURE 4
Methylotaxis and formtaxis rates of a series of MCP gene knockouts generated under the backgrounds of various MDH gene knockouts. Data are 
presented as the mean chemotaxis rate  ±  standard deviation (n = 3). nt, not tested.

## Page 8

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
08
frontiersin.org
bacteria cytoplasmic chemoreceptors had no identifiable domain, 
whereas about half of analyzed chemoreceptors contain PAS domain 
that is involved mainly in energy taxis (Collins et  al., 2014). 
Identification of the ligand for MtpA is currently underway.
MtpB was found to depend on MDH activity and La3+ (Figure 4). 
Its cellular localization changed in response to La3+ (Figure 1E), which 
is unique, as well as reasonable to detect the MDH activity that operate 
in the periplasm. The molecular mechanism that regulates and alters 
the protein localization is unknown. As one of the examples of 
differential localization of MCP protein, the Azospirillum brasilense 
aerotaxis sensor AerC exhibits different localization: the cell pole in 
the nitrogen fixation condition and the cytosol in the presence of 
ammonium (Xie et  al., 2010). The dCache_1 domain generally 
recognizes various compounds, and majority of known ligands are 
amino acids (Upadhyay et al., 2016). Because its activity depends on 
MDH activity, the ligand for MtpB is not methanol itself. MDH genes 
(mxaFI and xoxF1) are associated with solute-binding protein genes 
(mxaJ and xoxJ) in each cluster. mxaJ deletion in M. extorquens AM1 
resulted in disruption of MxaFI activation (Amaratunga et al., 1997). 
MxaJ is suggested to be crucial for MxaFI maturation, however, its 
exact role is unknown. On the other hand, solute binding proteins are 
known to function as ligands for many different types of signal 
transduction receptors, including MCPs that contain dCache, HBM 
or TarH domains (Matilla et al., 2021). Therefore, it is possible that the 
ligand for MtpB is XoxJ. MtpB is also involved in formtaxis and 
ethanol-taxis (Supplementary Figure S8) due to the formaldehyde and 
ethanol oxidation capacity of XoxF1. Ethanol is released from plants 
(Fall, 1999), and is also a good growth substrate for strain 22A 
(Yanpirat et al., 2020). Most probably, ethanol-taxis is dependent on 
MtpB and XoxF1 or ExaF activity. As we  reported previously, 
FIGURE 5
PmtpC activity in various MDH and ∆mxbD mutants. Strain 22A MDH knockouts and ∆mxbD mutant carrying pAT06-PmtpC were grown on methanol, 
succinate, or methanol plus succinate in the absence/presence of La3+ in liquid medium prepared in 96-well plates. The data were analyzed with 
analysis of variance followed by Dunnet’s test to compare the differences against wild-type data. p values lower than 0.01 are indicated by asterisks. 
The data are shown as mean luminescence/OD600  ±  SD (n  =  4). n.g., no growth.

## Page 9

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
09
frontiersin.org
Ln3+-dependent methylotrophy is completely conserved in the genera 
whereas some strains lack the mxa cluster (Alessa et al., 2021), and 
XoxF-type MDH is considered to be  ancestral to MxaF-type 
MDH. Therefore, it is reasonable that MtpB monitoring XoxF1 activity 
is conserved widely in the genera (Supplementary Table S1). MtpB is 
relatively less conserved in clade D members that have relatively 
smaller genomes as well as smaller numbers of MCPs. Clade D 
contains specialized forest tree phyllospheric members (Leducq et al., 
2022) that may have limited access to Ln3+.
MtpC was found to be associated with MxaF activity (Figure 4). 
Its expression is independent of mxaF expression but dependent on 
mxbD, which regulates mxaF expression in the absence of La3+ 
(Figure  6). Thus, mxbD regulates not only MxaF-dependent 
methylotrophy but also methylotaxis when Ln3+ is not available. As 
one of the similar regulators, ArcA from avian pathogenic E. coli also 
controls chemotaxis as well as metabolism and motility (Jiang et al., 
2015). Because MtpC cellular localization did not change in response 
to La3+, and its amino acid sequence does not contain any known 
domains, its mode of action may differ from that of MtpB. MtpC will 
not bind methanol directly as a ligand, and it is unknown how MtpC 
activity cooperates with MxaF activity. MtpC appeared randomly 
across the type strain genomes but not in the strains that lack mxa 
genes (M. tardum NBRC 103632T, M. longum DSM 23933T, 
M. persicinum NBRC 103628T, M. komagatae DSM 19563T, and 
M. iners DSM 19015T; Supplementary Table S1, Alessa et al., 2021), 
implying the functional and evolutionary link between MtpC 
and MxaFI.
Thus, strain 22A is equipped with as many as three distinct MCPs 
that enable its methylotaxis with different mechanisms. They navigate 
the cells to the niche where methanol is more available by monitoring 
FIGURE 6
A schematic representation of the putative mechanism of strain 22A methylotaxis. Methanol released by plants is oxidized to formaldehyde in the 
periplasm by either MxaF (with its beta subunit, MxaI) or XoxF1 depending on the availability of Ln3+. MtpA localizes in the cytosol and presumably 
recognizes formaldehyde as a ligand. MtpB is induced in the presence of Ln3+, and its activity is coupled with XoxF activity. MtpC is induced in the 
absence of Ln3+, and its activity is coupled with MxaF activity directly or indirectly. The expression of MtpC and MxaF is regulated under the control of 
MxbDM. The signals were integrated and transmitted to Che proteins that control the direction of flagellar rotation, resulting in methylotaxis and 
successful cell gathering to plants.

## Page 10

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
10
frontiersin.org
the cellular methanol oxidation and its product formaldehyde, 
depending on which MDH is operating in response to the availability 
of Ln3+. A schematic representation of possible methylotaxis 
mechanisms in strain 22A is provided in Figure 6.
Many kinds of plant-derived chemicals, including organic acids, 
amino acids, phenolics, and sugars, support plant-associated 
bacterial survival (Chaparro et  al., 2013). They have also been 
identified as cues for bacteria chemotaxis to locate the plants (Feng 
et al., 2018). Within such a wide variety of chemotaxis, we propose 
that methylotaxis is one of the crucial steps for methylotrophs to 
initiate symbiosis. Further investigation of ligand identification for 
methylotaxis MCPs, the roles of many other sensors encoded in the 
strain 22A genome, and the identification of other types of 
methylotaxis sensors in the other Methylobacterium species will 
contribute to revealing the eco-physiological and evolutionary 
versatility of Methylobacterium species.
Materials and methods
Strains and culture conditions
M. aquaticum strain 22A (FERM-BP11078, Tani et al., 2012) was 
used for MCP identification. Other Methylobacterium type strains 
were also tested for methylotaxis. Methylobacterium strains were 
usually grown on R2A medium or mineral medium (MM; Alamgir 
et al., 2015) containing 0.5% methanol or 0.5% succinate, or both. 
Kanamycin (25 mg/L) and 1 μM LaCl3 were added when necessary. 
For growth experiments, strain 22A and its derivatives were grown on 
200 μl medium prepared in 96-well plates, which were rotary-shaken 
at 300 rpm at 28°C. The growth was monitored by measuring optical 
density at 600 nm using a microplate reader (PowerScan HT, DS 
Pharma). MeOH-La and MeOH+La conditions refer to MM medium 
containing 0.5% methanol in the absence and presence of 1 μM LaCl3, 
respectively. E. coli DH5α was used for plasmid construction and 
E. coli S17-1 was used for conjugation, and they were grown on 
LB medium.
Gene knockouts
Gene knockout mutants for methanol dehydrogenases, that is, 
ΔmxaF, ΔxoxF1, ΔxoxF1Sup and ΔmxaFΔxoxF1, and mxbD, 
were generated in our previous studies (Masuda et  al., 2018; 
Yanpirat et al., 2020). Gene knockout mutants for MCP genes were 
generated using an allele-replacement vector pK18mobSacB, as 
previously reported (Alamgir et  al., 2015). In brief, the gene 
knockout vectors were constructed so that the vector contains 
tandem ligated each approximately 1 kb upstream and downstream 
regions of the gene to be  deleted, using the primers listed in 
Supplementary Table S2 and the In-Fusion Cloning kit (Takara 
Bio Co.). The vector was introduced into strain 22A via 
conjugation using E. coli S17-1. Single-crossover mutants were 
selected by kanamycin resistance, and double-crossover mutants 
were selected by sucrose resistance. Polymerase chain reaction 
diagnosis was carried out as described previously (Alamgir 
et al., 2015).
Chemotaxis assay
The cells grown on solid medium overnight were collected with a 
scraper, suspended in 2 to 3 ml of 10 mM HEPES pH 7.0 (OD600 = 0.01) 
in 15-ml tube, and incubated at 20°C for 2 h. Capillaries were made of 
a glass capillary (with filament, model GD-1, Narishige), with a glass 
puller (Narishige Model PC-10) so that the tip diameter becomes 10 
to 20 μm. NuSieve GTG agarose (Lonza Bioscience, Co.) was dissolved 
in 10 mM HEPES pH 7.0 (15 mg/ml) at 50°C. Methanol (and other 
substances) was added at the desired concentration (2% v/v or w/v, 
otherwise stated) and the solution was kept at 50°C under seal. When 
formaldehyde was used as a chemoattractant, 35 mg paraformaldehyde 
was dissolved in 175 μl 10 mM HEPES pH 7.0 and incubated at 120°C 
for 15 min, and the solution was regarded as 20% (w/v) formaldehyde. 
The capillary tip was soaked in the solution for 5 s, and rinsed with 
water. A sheet of FastWell™ (2 mm thickness, 20 mm diameter, Grace 
Bio-Labs) was placed on a slide glass, and the 170 μl cell suspension 
was pipetted into the well. The density of the cell suspension was 
appropriately adjusted so that 50 to 100 cells are evident in the 
microscopic window. A cover glass was placed offset, allowing a 
capillary inserted between the FastWell and the cover glass. The 
bacteria gathering at the capillary tip were monitored with a light 
microscope (×200 magnification, Olympus, Tokyo, Japan) for 3 or 
5 min, and pictured every 30 or 60 s (308 × 256 μm, 1,024 × 768 pixels) 
with a digital camera (VB-7010, Keyence). The cells in a frame were 
counted with ImageJ software (Schneider et al., 2012). Automatic cell 
counting was carried out with a macro containing the “Otsu” 
thresholding and “analyze particles” command. The assay was done in 
technical triplicates at least. The time-dependent gathering data were 
used to determine the intensity (gathering speed) of chemotaxis by 
measuring the slopes of the plots.
Chemotaxis toward plant tissues
The gathering and adhesion of strain 22A cells to rice or 
Arabidopsis thaliana roots were assessed as follows in technical 
triplicate. A. thaliana col-0 seeds were surface-sterilized with 70% 
ethanol (2 min), 7% sodium hypochlorite containing 0.2% Triton 
X-100 (8 min), and thorough washing with sterile water. The seeds 
were allowed to germinate on 1/2 Murashige-Skoog (MS) medium in 
square plates (14 cm × 10 cm) solidified with 1.2% agar at 23°C, for 
20 days (12 h light/dark cycle). The plates were set vertically to allow 
the roots to grow on the agar surface. The plants were removed, 
weighed, and rinsed with 10 mM HEPES pH 7.0. The root part only 
was soaked in 5 ml strain 22A cell suspension (OD600 = 0.01, 10 mM 
HEPES, pH 7.0, pre-grown in MeOH-La condition for 2 days) 
prepared in 6-well plates (1 plant/well). At appropriate intervals within 
0 to 20 (or 60) min, the root was transferred into 1 ml HEPES buffer 
in 1.5 ml tubes and homogenized with a pestle. The homogenates were 
serially diluted with 10 mM HEPES pH 7.0, and 10 μl of the dilutes 
were spread onto solid MM containing 0.5% methanol. The bacterial 
colony forming units (CFUs) were determined after 5 days of 
incubation at 28°C.
The experiment using rice roots was carried out similarly. Rice 
seeds were dehulled, soaked in 70% ethanol for 3 min, and incubated 
in 3% sodium hypochlorite containing 0.5% tween 20 at 80°C for 
30 min. The rice seeds (Oryza sativa cv. Nipponbare) were put on 0.8%

## Page 11

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
11
frontiersin.org
agar and allowed to grow at 28°C for 10 days. The excised rice roots 
were incubated in bacterial cell suspension and transferred into 5 ml 
HEPES containing 0.05% Sylwet (BioMedical Science, Tokyo) and 
vigorously vortexed for 10 s to remove the cells.
The density (CFU/ml) of the cell suspension (5 ml) was wild type 
2.5 ± 0.63 × 105 and TM 3.2 ± 0.26 × 105 in the Arabidopsis experiment, 
and wild type 2.0 ± 0.18 × 106 and TM 1.4 ± 0.21 × 106 in rice experiment.
A young leaf of A. thaliana grown as above was excised and put 
onto a slide glass, onto which strain 22A cell suspension was added. 
The bacterial cells were observed under a stereo microscope 
(Olympus MVX10).
Quantification and observation of 
mVenus-labeled cells on red perilla leaves
The DNA fragment encoding mVenus protein was amplified by 
polymerase chain reaction using pDAS2V (Takeya et al., 2018) as a 
template and cloned into the EcoRI-digested pAT02m (Yanpirat et al., 
2020) by the In-Fusion cloning kit. The plasmid, pAT02-V, was 
introduced into strains 22A and TM by electroporation (2 kV, 25 μF, 
200 Ω) using a Gene Pulser Xcell (Bio-Rad Laboratories, Hercules, 
CA). Red perilla (Perilla frutescens crispa [Thunb.] Makino) seeds 
were sterilized with 70% ethanol for 1 min, and with 1% sodium 
hypochlorite (containing 0.3% Tween 20) for 1 min, then washed with 
sterilized water 5 times. Strains 22A and TM were cultivated in MM 
containing 0.5% methanol and 20 μg/ml kanamycin for 2 days at 28°C 
and cells were collected, washed with sterilized water, and suspended 
in sterilized water to obtain cell suspensions with OD610 of 0.1. The 
sterilized red perilla seeds were soaked in the cell suspension of strains 
22A or TM for 3 h with gentle shaking at 2 rpm using a Rotator RT-5 
(Taitec, Saitama, Japan) at room temperature. The treated seeds were 
sown onto Hoagland agar (culture dish, 100 mm × 40 mm, with porous 
film seal) and aseptically grown in a chamber (NK Biotron LH-220S, 
Nippon Medical and Chemical Instruments, Osaka, Japan) for 
112 days. The system was operated at 25°C under a 16 h light and 8 h 
dark cycle.
Fresh leaves were removed from the perilla plants aseptically, put 
into a 1.5 ml tube, and weighed. Phosphate-buffered saline (PBS) was 
added to the tube (100 μl/10 mg leaf) and vigorously mixed with a Vortex 
mixer for 15 min. The 30 μl of suspension and 30 μl of AccuCheck 
Counting Beads (ThermoFisher Scientific, MA) were added to 300 μl of 
PBS, and mVenus-labeled cells were counted by flow cytometry 
(FACSAria IIIu, Becton Dickinson, San Jose, CA). For observation by 
fluorescence microscopy, one fresh leaf was impressed onto a solid MM 
containing 0.5% methanol and 20 μg/ml kanamycin for 1 min. After 
removal of the leaf, the plates were incubated for several days at 28°C and 
colonies were observed with a fluorescence stereo-microscope (Olympus 
SZ16) equipped with a digital charge-coupled device camera (Olympus 
DP80) and a YFP filter (Olympus SZX2-FYFPHQ).
Promoter-reporter assay
The polymerase chain reaction–generated DNA of the mtpC 
promoter region (upstream non-coding region of the gene, 455 bp) was 
cloned into the NcoI site on pAT06-Lux that is a promoter-less bacterial 
luciferase reporter vector (Juma et al., 2022). The vector (pAT06-PmtpC) 
was introduced into strain 22A derivatives via conjugation using E. coli 
S17-1 and selected on kanamycin. The transformants were grown in 
200 μl MM containing methanol or succinate or both, in the presence or 
absence of LaCl3. The culture OD600 and luminescence were measured 
with a microplate reader (PowerScan HT, DS Pharma). The promoter 
activity was regarded as the luminescence / OD600 when the luminescence 
reached a maximum during the cultivation.
Cellular MCP localization analysis
To observe the cellular localization of MCPs, mtpA (maq22A_
c14925), mtpB (maq22A_1p32440), and mtpC (maq22A_c15300) 
genes with their promoter region were cloned in tandem with the GFP 
gene into the PstI site of pCM130KmC (Yanpirat et al., 2020) using the 
In-Fusion technique and the primers listed in Supplementary Table S2 
to generate pCM130KmC-MtpA (or MtpB and MtpC)-GFP. The 
plasmids were transferred into strain 22A wild type or TM via 
conjugation by E. coli S17-1 and grown on 0.5% methanol in MM for 
1 day. The cells were subjected to confocal microscopic observation 
(FV1000, Olympus). As a control, the GFP ORF fragment (without its 
promoter) was cloned into pCM130KmC.
Gene complementation
The methylotaxis protein genes and their promoter regions were 
each PCR-amplified with the primers listed in Supplementary Table S2, 
and cloned into EcoRI site of pAT01 that enables His-tagged protein 
expression in M. aquaticum strain 22A (Fujitani et  al., 2022). 
We introduced termination codon in the 3′ primers to avoid possible 
MCP activity interference by the tag. The vectors were each introduced 
into TM, and the transformants were grown on methanol in the 
presence and absence of LaCl3 and subjected to methylotaxis assay.
Methylotaxis MCP homologs in 
Methylobacterium genomes
We sought MCP genes in the genomes of 62 Methylobacterium 
type strains using 52 amino acid sequences of strain 22A MCPs by 
BlastP (40% identity threshold). We found 1,467 MCP genes in total. 
MCPs with more than 60% identity to strain 22A methylotaxis MCPs 
were counted as methylotaxis MCP homologs.
Statistical analysis
The statistical analysis of data (Student’s t-test and analysis of 
variance) was carried out using Prism 6 (GraphPad Software, Inc., 
CA, USA).
Data availability statement
The original contributions presented in the study are included in 
the article/Supplementary material, further inquiries can be directed 
to the corresponding author.

## Page 12

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
12
frontiersin.org
Author contributions
AT: Conceptualization, Data curation, Formal analysis, Funding 
acquisition, Investigation, Methodology, Project administration, 
Resources, Supervision, Validation, Visualization, Writing – original 
draft, Writing – review & editing. SM: Conceptualization, 
Investigation, Methodology, Writing – review & editing. YF: 
Investigation, Methodology, Writing – review & editing. TI: 
Investigation, Methodology, Writing – original draft, Writing – review 
& editing. YH: Investigation, Methodology, Writing – original draft, 
Writing – review & editing. SKi: Investigation, Methodology, Writing 
– original draft, Writing – review & editing. WS: Investigation, 
Methodology, Writing – original draft, Writing – review & editing. 
HL: Investigation, Methodology, Writing – original draft, Writing – 
review & editing. SKa: Investigation, Methodology, Writing – original 
draft, Writing – review & editing. HY: Conceptualization, 
Investigation, Methodology, Writing – original draft, Writing – review 
& editing. YS: Conceptualization, Investigation, Supervision, Writing 
– original draft, Writing – review & editing. JK: Conceptualization, 
Investigation, Methodology, Writing – original draft, Writing – review 
& editing.
Funding
The author(s) declare financial support was received for the 
research, authorship, and/or publication of this article. This work was 
supported in part by MEXT KAKENHI (21H02105 to AT), Advanced 
Low Carbon Technology Research and Development Program 
(ALCA) JST, the Joint Usage/Research Center, Institute of Plant 
Science and Resources, Okayama University, and Wesco Scientific 
Promotion Foundation.
Conflict of interest
The authors declare that the research was conducted in the 
absence of any commercial or financial relationships that could 
be construed as a potential conflict of interest.
Publisher’s note
All claims expressed in this article are solely those of the 
authors and do not necessarily represent those of their affiliated 
organizations, or those of the publisher, the editors and the 
reviewers. Any product that may be evaluated in this article, or 
claim that may be made by its manufacturer, is not guaranteed or 
endorsed by the publisher.
Supplementary material
The Supplementary material for this article can be found online at:
https://www.frontiersin.org/articles/10.3389/fmicb.2023.1258452/
full#supplementary-material
References
Alamgir, K. M., Masuda, S., Fujitani, Y., Fukuda, F., and Tani, A. (2015). Production 
of ergothioneine by Methylobacterium species. Front. Microbiol. 6:1185. doi: 10.3389/
fmicb.2015.01185
Alessa, O., Ogura, Y., Fujitani, Y., Takami, H., Hayashi, T., Sahin, N., et al. (2021). 
Comprehensive comparative genomics and phenotyping of Methylobacterium species. 
Front. Microbiol. 12:740610. doi: 10.3389/fmicb.2021.740610
Allard-Massicotte, R., Tessier, L., Lécuyer, F., Lakshmanan, V., Lucier, J. F., Garneau, D., 
et al. (2016). Bacillus subtilis early colonization of Arabidopsis thaliana roots involves 
multiple chemotaxis receptors. MBio 7, e01664–e01616. doi: 10.1128/mBio.01664-16
Amaratunga, K., Goodwin, P. M., O'Connor, C. D., and Anthony, C. (1997). The 
methanol oxidation genes mxaFJGIR(S)ACKLD in Methylobacterium extorquens. FEMS 
Microbiol. Lett. 146, 31–38. doi: 10.1111/j.1574-6968.1997.tb10167.x
Anderson, D. J., Morris, C. J., Nunn, D. N., Anthony, C., and Lidstrom, M. E. (1990). 
Nucleotide sequence of the Methylobacterium extorquens AM1 moxF and moxJ genes 
involved in methanol oxidation. Gene 90, 173–176. doi: 10.1016/0378-1119(90)90457-3
Blunden, G., Carpenter, B. G., Adrian-Romero, M., Yang, M. H., and Tyihák, E. (1998). 
Formaldehyde in the plant kingdom. Acta Biol. Hung. 49, 239–246. doi: 10.1007/
BF03542997
Briegel, A., Ortega, D. R., Tocheva, E. I., Wuichet, K., Li, Z., Chen, S., et al. (2009). 
Universal architecture of bacterial chemoreceptor arrays. Proc. Natl. Acad. Sci. U. S. A. 
106, 17181–17186. doi: 10.1073/pnas.0905181106
Chaparro, J. M., Badri, D. V., Bakker, M. G., Sugiyama, A., Manter, D. K., and 
Vivanco, J. M. (2013). Root exudation of phytochemicals in Arabidopsis follows specific 
patterns that are developmentally programmed and correlate with soil microbial 
functions. PLoS One 8:e55731. doi: 10.1371/journal.pone.0055731
Chi, F., Shen, S. H., Cheng, H. P., Jing, Y. X., Yanni, Y. G., and Dazzo, F. B. (2005). 
Ascending migration of endophytic rhizobia, from roots to leaves, inside rice plants and 
assessment of benefits to rice growth physiology. Appl. Environ. Microbiol. 71, 
7271–7278. doi: 10.1128/AEM.71.11.7271-7278.2005
Chistoserdova, L. (2019). New pieces to the lanthanide puzzle. Mol. Microbiol. 111, 
1127–1131. doi: 10.1111/mmi.14210
Collins, K. D., Lacal, J., and Ottemann, K. M. (2014). Internal sense of direction: 
sensing and signaling from cytoplasmic chemoreceptors. Microbiol. Mol. Biol. Rev. 78, 
672–684. doi: 10.1128/MMBR.00033-14
Dourado, M. N., Camargo Neves, A. A., Santos, D. S., and Araújo, W. L. (2015). 
Biotechnological and agronomic potential of endophytic pink-pigmented 
methylotrophic Methylobacterium spp. Biomed. Res. Int. 2015:909016. doi: 
10.1155/2015/909016
Fall, R. (1999). “Chapter 2-Biogenic emissions of volatile organic compounds from 
higher plants” in Reactive hydrocarbons in the atmosphere. ed. C. N. Hewitt (Academic 
Press), 41–96.
Fall, R., and Benson, A. A. (1996). Leaf methanol - the simplest natural product from 
plants. Trends Plant Sci. 1, 296–301. doi: 10.1016/S1360-1385(96)88175-0
Feng, H., Zhang, N., Du, W., Zhang, H., Liu, Y., Fu, R., et al. (2018). Identification of 
chemotaxis compounds in root exudates and their sensing chemoreceptors in plantgrowth-promoting rhizobacteria Bacillus amyloliquefaciens SQR9. Mol. Plant-Microbe 
Interact. 31, 995–1005. doi: 10.1094/MPMI-01-18-0003-R
Feng, H., Zhang, N., Fu, R., Liu, Y., Krell, T., Du, W., et al. (2019). Recognition of 
dominant attractants by key chemoreceptors mediates recruitment of plant growthpromoting rhizobacteria. Environ. Microbiol. 21, 402–415. doi: 10.1111/1462-2920.14472
Fujitani, Y., Shibata, T., and Tani, A. (2022). A periplasmic lanthanide mediator, 
lanmodulin, in Methylobacterium aquaticum strain 22A. Front. Microbiol. 13:921636. 
doi: 10.3389/fmicb.2022.921636
Good, N. M., Vu, H. N., Suriano, C. J., Subuyuj, G. A., Skovran, E., and 
Martinez-Gomez, N. C. (2016). Pyrroloquinoline quinone ethanol dehydrogenase in 
Methylobacterium extorquens AM1 extends lanthanide-dependent metabolism to 
multicarbon substrates. J. Bacteriol. 198, 3109–3118. doi: 10.1128/JB.00478-16
Hibi, Y., Asai, K., Arafuka, H., Hamajima, M., Iwama, T., and Kawai, K. (2011). 
Molecular structure of La3+-induced methanol dehydrogenase-like protein in 
Methylobacterium radiotolerans. J. Biosci. Bioeng. 111, 547–549. doi: 10.1016/j.
jbiosc.2010.12.017
Ji, K. X., Chi, F., Yang, M. F., Shen, S. H., Jing, Y. X., Dazzo, F. B., et al. (2010). 
Movement of rhizobia inside tobacco and lifestyle alternation from endophytes to freeliving rhizobia on leaves. J. Microbiol. Biotechnol. 20, 238–244. doi: 10.4014/
jmb.0906.06042
Jiang, F., An, C., Bao, Y., Zhao, X., Jernigan, R. L., Lithio, A., et al. (2015). ArcA 
controls metabolism, chemotaxis, and motility contributing to the pathogenicity of avian 
pathogenic Escherichia coli. Infect. Immun. 83, 3545–3554. doi: 10.1128/IAI.00312-15

## Page 13

Tani et al.
10.3389/fmicb.2023.1258452
Frontiers in Microbiology
13
frontiersin.org
Juma, P. O., Fujitani, Y., Alessa, O., Oyama, T., Yurimoto, H., Sakai, Y., et al. (2022). 
Siderophore for lanthanide and iron uptake for methylotrophy and plant growth 
promotion in Methylobacterium aquaticum strain 22A. Front. Microbiol. 13:921635. doi: 
10.3389/fmicb.2022.921635
Kamenopoulos, S. N., Shields, D., and Agioutantis, Z. (2016). “Sustainable 
development criteria and indicators for the assessment of rare earth element mining 
projects” in Rare earths industry. Technological, economic, and environmental 
implications. De Lima, B. I. and Filho, L. W. (Eds). (Netherlands: Elsevier Inc), 87–109. 
doi: 10.1016/B978-0-12-802328-0.00006-1
Karmakar, R. (2021). State of the art of bacterial chemotaxis. J. Basic Microbiol. 61, 
366–379. doi: 10.1002/jobm.202000661
Keltjens, J. T., Pol, A., Reimann, J., and Op den Camp, H. J. (2014). PQQ-dependent 
methanol dehydrogenases: rare-earth elements make a difference. Appl. Microbiol. 
Biotechnol. 98, 6163–6183. doi: 10.1007/s00253-014-5766-8
Lacal, J., García-Fontana, C., Muñoz-Martínez, F., Ramos, J. L., and Krell, T. (2010). 
Sensing of environmental signals: classification of chemoreceptors according to the size 
of their ligand binding regions. Environ. Microbiol. 12, 2873–2884. doi: 
10.1111/j.1462-2920.2010.02325.x
Leducq, J. B., Sneddon, D., Santos, M., Condrain-Morel, D., Bourret, G., 
Martinez-Gomez, N. C., et al. (2022). Comprehensive phylogenomics of 
Methylobacterium reveals four evolutionary distinct groups and underappreciated 
phyllosphere diversity. Genome Biol. Evol. 14:evac123. doi: 10.1093/gbe/evac123
Long, Z., Quaife, B., Salman, H., and Oltvai, Z. N. (2017). Cell-cell communication 
enhances bacterial chemotaxis toward external attractants. Sci. Rep. 7:12855. doi: 
10.1038/s41598-017-13183-9.hw
Masuda, S., Suzuki, Y., Fujitani, Y., Mitsui, R., Nakagawa, T., Shintani, M., et al. (2018). 
Lanthanide-dependent regulation of methylotrophy in Methylobacterium aquaticum 
strain 22A. mSphere 3, e00462–e00417. doi: 10.1128/mSphere.00462-17
Matilla, M. A., Ortega, Á., and Krell, T. (2021). The role of solute binding proteins in 
signal transduction. Comput. Struct. Biotechnol. J. 19, 1786–1805. doi: 10.1016/j.
csbj.2021.03.029
Nakagawa, T., Mitsui, R., Tani, A., Sasa, K., Tashiro, S., Iwama, T., et al. (2012). A 
catalytic role of XoxF1 as La3+-dependent methanol dehydrogenase in Methylobacterium 
extorquens strain AM1. PLoS One 7:e50480. doi: 10.1371/journal.pone.0050480
Ochsner, A. M., Hemmerle, L., Vonderach, T., Nüssli, R., Bortfeld-Miller, M., 
Hattendorf, B., et al. (2019). Use of rare-earth elements in the phyllosphere colonizer 
Methylobacterium extorquens PA1. Mol. Microbiol. 111, 1152–1166. doi: 10.1111/mmi.14208
Parkinson, J. S. (2010). Signaling mechanisms of HAMP domains in chemoreceptors and 
sensor kinases. Annu. Rev. Microbiol. 64, 101–122. doi: 10.1146/annurev.micro.112408.134215
Roszczenko-Jasińska, P., Vu, H. N., Subuyuj, G. A., Crisostomo, R. V., Cai, J., 
Lien, N. F., et al. (2020). Gene products and processes contributing to lanthanide 
homeostasis and methanol metabolism in Methylorubrum extorquens AM1. Sci. Rep. 
10:12663. doi: 10.1038/s41598-020-69401-4
Scharf, B. E., Hynes, M. F., and Alexandre, G. M. (2016). Chemotaxis signaling systems 
in model beneficial plant-bacteria associations. Plant Mol. Biol. 90, 549–559. doi: 
10.1007/s11103-016-0432-4
Schneider, C. A., Rasband, W. S., and Eliceiri, K. W. (2012). NIH image to ImageJ: 25 
years of image analysis. Nat. Methods 9, 671–675. doi: 10.1038/nmeth.2089
Skovran, E., Palmer, A. D., Rountree, A. M., Good, N. M., and Lidstrom, M. E. (2011). 
XoxF is required for expression of methanol dehydrogenase in Methylobacterium 
extorquens AM1. J. Bacteriol. 193, 6032–6038. doi: 10.1128/JB.05367-11
Skovran, E., Raghuraman, C., and Martinez-Gomez, N. C. (2019). Lanthanides in 
methylotrophy. Curr. Issues Mol. Biol. 33, 101–116. doi: 10.21775/cimb.033.101
Sourjik, V., and Armitage, J. P. (2010). Spatial organization in bacterial chemotaxis. 
EMBO J. 29, 2724–2733. doi: 10.1038/emboj.2010.178
Takeya, T., Yurimoto, H., and Sakai, Y. (2018). A Pichia pastoris single-cell biosensor 
for detection of enzymatically produced methanol. Appl. Microbiol. Biotechnol. 102, 
7017–7027. doi: 10.1007/s00253-018-9144-9
Tani, A., Mitsui, R., and Nakagawa, T. (2021). Discovery of lanthanide-dependent 
methylotrophy and screening methods for lanthanide-dependent methylotrophs. 
Methods Enzymol. 650, 1–18. doi: 10.1016/bs.mie.2021.01.031
Tani, A., Ogura, Y., Hayashi, T., and Kimbara, K. (2015). Complete genome sequence 
of Methylobacterium aquaticum strain 22A, isolated from Racomitrium japonicum 
moss. Genome Announc. 3:e00266–15. doi: 10.1128/genomeA.00266-15
Tani, A., Takai, Y., Suzukawa, I., Akita, M., Murase, H., and Kimbara, K. (2012). 
Practical application of methanol-mediated mutualistic symbiosis between 
Methylobacterium species and a roof greening moss, Racomitrium japonicum. PLoS One 
7:e33800. doi: 10.1371/journal.pone.0033800
Tola, Y. H., Fujitani, Y., and Tani, A. (2019). Bacteria with natural chemotaxis towards 
methanol revealed by chemotaxis fishing technique. Biosci. Biotechnol. Biochem. 83, 
2163–2171. doi: 10.1080/09168451.2019.1637715
Upadhyay, A. A., Fleetwood, A. D., Adebali, O., Finn, R. D., and Zhulin, I. B. (2016). 
Cache domains that are homologous to, but different from PAS domains comprise the 
largest superfamily of extracellular sensors in prokaryotes. PLoS Comput. Biol. 
12:e1004862. doi: 10.1371/journal.pcbi.1004862
Vorholt, J. A. (2012). Microbial life in the phyllosphere. Nat. Rev. Microbiol. 10, 
828–840. doi: 10.1038/nrmicro2910
Vu, H. N., Subuyuj, G. A., Vijayakumar, S., Good, N. M., Martinez-Gomez, N. C., and 
Skovran, E. (2016). Lanthanide-dependent regulation of methanol oxidation systems in 
Methylobacterium extorquens AM1 and their contribution to methanol growth. J. 
Bacteriol. 198, 1250–1259. doi: 10.1128/JB.00937-15
Wang, H., Zhang, M., Xu, Y., Zong, R., Xu, N., and Guo, M. (2021). Agrobacterium 
fabrum atu0526-encoding protein is the only chemoreceptor that regulates 
chemoattraction toward the broad antibacterial agent formic acid. Biology 10:1345. doi: 
10.3390/biology10121345
Xie, Z., Ulrich, L. E., Zhulin, I. B., and Alexandre, G. (2010). PAS domain containing 
chemoreceptor couples dynamic changes in metabolism with chemotaxis. Proc. Natl. 
Acad. Sci. U. S. A. 107, 2235–2240. doi: 10.1073/pnas.0910055107
Yanpirat, P., Nakatsuji, Y., Hiraga, S., Fujitani, Y., Izumi, T., Masuda, S., et al. (2020). 
Lanthanide-dependent methanol and formaldehyde oxidation in Methylobacterium 
aquaticum strain 22A. Microorganisms 8:822. doi: 10.3390/microorganisms8060822

