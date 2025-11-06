Feature: Chat Evaluation with SQuAD v2.0 Dataset
  As a user of the KETA system
  I want to evaluate the conversation agent using SQuAD v2.0 questions
  So that I can measure the quality of responses using DeepEval metrics

  Background: Setup for SQuAD evaluation scenarios
    Given the API is running
    And I have created an objective with name "SQuAD Evaluation"

  Scenario: SQuAD Sample 1 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 1" and content "Other important complexity classes include BPP, ZPP and RP, which are defined using probabilistic Turing machines; AC and NC, which are defined using Boolean circuits; and BQP and QMA, which are defined using quantum Turing machines. #P is an important complexity class of counting problems (not decision problems). Classes like IP and AM are defined using Interactive proof systems. ALL is the class of all decision problems."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 1 Chat"
    When I send a message with content "BQP and QMA are examples of complexity classes most commonly associated with what type of Turing machine?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "quantum"

  Scenario: SQuAD Sample 2 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 2" and content "Subsequently, Californios (dissatisfied with inequitable taxes and land laws) and pro-slavery southerners in the lightly populated \"Cow Counties\" of southern California attempted three times in the 1850s to achieve a separate statehood or territorial status separate from Northern California. The last attempt, the Pico Act of 1859, was passed by the California State Legislature and signed by the State governor John B. Weller. It was approved overwhelmingly by nearly 75% of voters in the proposed Territory of Colorado. This territory was to include all the counties up to the then much larger Tulare County (that included what is now Kings, most of Kern, and part of Inyo counties) and San Luis Obispo County. The proposal was sent to Washington, D.C. with a strong advocate in Senator Milton Latham. However, the secession crisis following the election of Abraham Lincoln in 1860 led to the proposal never coming to a vote."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 2 Chat"
    When I send a message with content "Who was the governor of California in 1895?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 3 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 3" and content "2013 Economics Nobel prize winner Robert J. Shiller said that rising inequality in the United States and elsewhere is the most important problem. Increasing inequality harms economic growth. High and persistent unemployment, in which inequality increases, has a negative effect on subsequent long-run economic growth. Unemployment can harm growth not only because it is a waste of resources, but also because it generates redistributive pressures and subsequent distortions, drives people to poverty, constrains liquidity limiting labor mobility, and erodes self-esteem promoting social dislocation, unrest and conflict. Policies aiming at controlling unemployment and in particular at reducing its inequality-associated effects support economic growth."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 3 Chat"
    When I send a message with content "Persistent unemployment has what effect on long-term economic growth?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "negative"

  Scenario: SQuAD Sample 4 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 4" and content "Philosophers in antiquity used the concept of force in the study of stationary and moving objects and simple machines, but thinkers such as Aristotle and Archimedes retained fundamental errors in understanding force. In part this was due to an incomplete understanding of the sometimes non-obvious force of friction, and a consequently inadequate view of the nature of natural motion. A fundamental error was the belief that a force is required to maintain motion, even at a constant velocity. Most of the previous misunderstandings about motion and force were eventually corrected by Galileo Galilei and Sir Isaac Newton. With his mathematical insight, Sir Isaac Newton formulated laws of motion that were not improved-on for nearly three hundred years. By the early 20th century, Einstein developed a theory of relativity that correctly predicted the action of forces on objects with increasing momenta near the speed of light, and also provided insight into the forces produced by gravitation and inertia."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 4 Chat"
    When I send a message with content "Something that is considered a non fundamental error is the belief that a force is required to maintain what?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 5 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 5" and content "On August 15, 1971, the United States unilaterally pulled out of the Bretton Woods Accord. The US abandoned the Gold Exchange Standard whereby the value of the dollar had been pegged to the price of gold and all other currencies were pegged to the dollar, whose value was left to \"float\" (rise and fall according to market demand). Shortly thereafter, Britain followed, floating the pound sterling. The other industrialized nations followed suit with their respective currencies. Anticipating that currency values would fluctuate unpredictably for a time, the industrialized nations increased their reserves (by expanding their money supplies) in amounts far greater than before. The result was a depreciation of the dollar and other industrialized nations' currencies. Because oil was priced in dollars, oil producers' real income decreased. In September 1971, OPEC issued a joint communiqué stating that, from then on, they would price oil in terms of a fixed amount of gold."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 5 Chat"
    When I send a message with content "What did the US abandon? "
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 6 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 6" and content "In cases where the criminalized behavior is pure speech, civil disobedience can consist simply of engaging in the forbidden speech. An example would be WBAI's broadcasting the track \"Filthy Words\" from a George Carlin comedy album, which eventually led to the 1978 Supreme Court case of FCC v. Pacifica Foundation. Threatening government officials is another classic way of expressing defiance toward the government and unwillingness to stand for its policies. For example, Joseph Haas was arrested for allegedly sending an email to the Lebanon, New Hampshire city councilors stating, \"Wise up or die.\""
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 6 Chat"
    When I send a message with content "What did Joseph Haas say in his email?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "\"Wise up or die.\""

  Scenario: SQuAD Sample 7 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 7" and content "The concept of legal certainty is recognised one of the general principles of European Union law by the European Court of Justice since the 1960s. It is an important general principle of international law and public law, which predates European Union law. As a general principle in European Union law it means that the law must be certain, in that it is clear and precise, and its legal implications foreseeable, specially when applied to financial obligations. The adoption of laws which will have legal effect in the European Union must have a proper legal basis. Legislation in member states which implements European Union law must be worded so that it is clearly understandable by those who are subject to the law. In European Union law the general principle of legal certainty prohibits Ex post facto laws, i.e. laws should not take effect before they are published. The doctrine of legitimate expectation, which has its roots in the principles of legal certainty and good faith, is also a central element of the general principle of legal certainty in European Union law. The legitimate expectation doctrine holds that and that \"those who act in good faith on the basis of law as it is or seems to be should not be frustrated in their expectations\"."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 7 Chat"
    When I send a message with content "What must the adoption of laws which will have legal effect in the EU have?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "a proper legal basis"

  Scenario: SQuAD Sample 8 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 8" and content "In 1564 a group of Norman Huguenots under the leadership of Jean Ribault established the small colony of Fort Caroline on the banks of the St. Johns River in what is today Jacksonville, Florida. The effort was the first at any permanent European settlement in the present-day continental United States, but survived only a short time. A September 1565 French naval attack against the new Spanish colony at St. Augustine failed when its ships were hit by a hurricane on their way to the Spanish encampment at Fort Matanzas. Hundreds of French soldiers were stranded and surrendered to the numerically inferior Spanish forces led by Pedro Menendez. Menendez proceeded to massacre the defenseless Huguenots, after which he wiped out the Fort Caroline garrison."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 8 Chat"
    When I send a message with content "From where had the Norman Huguenots sailed in order to arrive at Fort Caroline?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 9 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 9" and content "The College of the University of Chicago grants Bachelor of Arts and Bachelor of Science degrees in 50 academic majors and 28 minors. The college's academics are divided into five divisions: the Biological Sciences Collegiate Division, the Physical Sciences Collegiate Division, the Social Sciences Collegiate Division, the Humanities Collegiate Division, and the New Collegiate Division. The first four are sections within their corresponding graduate divisions, while the New Collegiate Division administers interdisciplinary majors and studies which do not fit in one of the other four divisions."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 9 Chat"
    When I send a message with content "Which University's College grants academic minors in 50 subject areas?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 10 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 10" and content "Along the same lines, co-NP is the class containing the complement problems (i.e. problems with the yes/no answers reversed) of NP problems. It is believed that NP is not equal to co-NP; however, it has not yet been proven. It has been shown that if these two complexity classes are not equal then P is not equal to NP."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 10 Chat"
    When I send a message with content "What implication can be derived for P and NP if P and co-NP are established to be unequal?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "P is not equal to NP"

  Scenario: SQuAD Sample 11 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 11" and content "Around 1685, Huguenot refugees found a safe haven in the Lutheran and Reformed states in Germany and Scandinavia. Nearly 50,000 Huguenots established themselves in Germany, 20,000 of whom were welcomed in Brandenburg-Prussia, where they were granted special privileges (Edict of Potsdam) and churches in which to worship (such as the Church of St. Peter and St. Paul, Angermünde) by Frederick William, Elector of Brandenburg and Duke of Prussia. The Huguenots furnished two new regiments of his army: the Altpreußische Infantry Regiments No. 13 (Regiment on foot Varenne) and 15 (Regiment on foot Wylich). Another 4,000 Huguenots settled in the German territories of Baden, Franconia (Principality of Bayreuth, Principality of Ansbach), Landgraviate of Hesse-Kassel, Duchy of Württemberg, in the Wetterau Association of Imperial Counts, in the Palatinate and Palatinate-Zweibrücken, in the Rhine-Main-Area (Frankfurt), in modern-day Saarland; and 1,500 found refuge in Hamburg, Bremen and Lower Saxony. Three hundred refugees were granted asylum at the court of George William, Duke of Brunswick-Lüneburg in Celle."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 11 Chat"
    When I send a message with content "What protestant religions made Northern European counties safe for Huguenot immigration?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Lutheran and Reformed"

  Scenario: SQuAD Sample 12 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 12" and content "Huguenot immigrants did not disperse or settle in different parts of the country, but rather, formed three societies or congregations; one in the city of New York, another 21 miles north of New York in a town which they named New Rochelle, and a third further upstate in New Paltz. The \"Huguenot Street Historic District\" in New Paltz has been designated a National Historic Landmark site and contains the oldest street in the United States of America. A small group of Huguenots also settled on the south shore of Staten Island along the New York Harbor, for which the current neighborhood of Huguenot was named."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 12 Chat"
    When I send a message with content "What is located within this district?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "the oldest street in the United States of America"

  Scenario: SQuAD Sample 13 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 13" and content "There is evidence that there have been significant changes in Amazon rainforest vegetation over the last 21,000 years through the Last Glacial Maximum (LGM) and subsequent deglaciation. Analyses of sediment deposits from Amazon basin paleolakes and from the Amazon Fan indicate that rainfall in the basin during the LGM was lower than for the present, and this was almost certainly associated with reduced moist tropical vegetation cover in the basin. There is debate, however, over how extensive this reduction was. Some scientists argue that the rainforest was reduced to small, isolated refugia separated by open forest and grassland; other scientists argue that the rainforest remained largely intact but extended less far to the north, south, and east than is seen today. This debate has proved difficult to resolve because the practical limitations of working in the rainforest mean that data sampling is biased away from the center of the Amazon basin, and both explanations are reasonably well supported by the available data."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 13 Chat"
    When I send a message with content "How has this debate been proven?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "This debate has proved difficult"

  Scenario: SQuAD Sample 14 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 14" and content "Legally, only non-profit trusts and societies can run schools in India. They will have to satisfy a number of infrastructure and human resource related criteria to get Recognition (a form of license) from the government. Critics of this system point out that this leads to corruption by school inspectors who check compliance and to fewer schools in a country that has the largest adult illiterate population in the world. While official data does not capture the real extent of private schooling in the country, various studies have reported unpopularity of government schools and an increasing number of private schools. The Annual Status of Education Report (ASER), which evaluates learning levels in rural India, has been reporting poorer academic achievement in government schools than in private schools. A key difference between the government and private schools is that the medium of education in private schools is English while it is the local language in government schools."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 14 Chat"
    When I send a message with content "Who can legally teach English in India?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 15 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 15" and content "The shortcomings of Aristotelian physics would not be fully corrected until the 17th century work of Galileo Galilei, who was influenced by the late Medieval idea that objects in forced motion carried an innate force of impetus. Galileo constructed an experiment in which stones and cannonballs were both rolled down an incline to disprove the Aristotelian theory of motion early in the 17th century. He showed that the bodies were accelerated by gravity to an extent that was independent of their mass and argued that objects retain their velocity unless acted on by a force, for example friction."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 15 Chat"
    When I send a message with content "What force acted on bodies to retard their velocity?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "friction"

  Scenario: SQuAD Sample 16 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 16" and content "The exodus of Huguenots from France created a brain drain, as many Huguenots had occupied important places in society. The kingdom did not fully recover for years. The French crown's refusal to allow non-Catholics to settle in New France may help to explain that colony's slow rate of population growth compared to that of the neighbouring British colonies, which opened settlement to religious dissenters. By the time of the French and Indian War (the North American front of the Seven Years' War), a sizeable population of Huguenot descent lived in the British colonies, and many participated in the British defeat of New France in 1759-60."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 16 Chat"
    When I send a message with content "The French and Indian War was the New World aspect of what European conflict?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Seven Years' War"

  Scenario: SQuAD Sample 17 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 17" and content "However, attempting to reconcile electromagnetic theory with two observations, the photoelectric effect, and the nonexistence of the ultraviolet catastrophe, proved troublesome. Through the work of leading theoretical physicists, a new theory of electromagnetism was developed using quantum mechanics. This final modification to electromagnetic theory ultimately led to quantum electrodynamics (or QED), which fully describes all electromagnetic phenomena as being mediated by wave–particles known as photons. In QED, photons are the fundamental exchange particle, which described all interactions relating to electromagnetism including the electromagnetic force.[Note 4]"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 17 Chat"
    When I send a message with content "What was used to create a new electromagnetic theory to reconcile the troubles with electromagnetic theory as it used to stand?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "quantum mechanics"

  Scenario: SQuAD Sample 18 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 18" and content "Approximately one million Protestants in modern France represent some 2% of its population. Most are concentrated in Alsace in northeast France and the Cévennes mountain region in the south, who still regard themselves as Huguenots to this day.[citation needed] A diaspora of French Australians still considers itself Huguenot, even after centuries of exile. Long integrated into Australian society, it is encouraged by the Huguenot Society of Australia to embrace and conserve its cultural heritage, aided by the Society's genealogical research services."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 18 Chat"
    When I send a message with content "How many protestants live in France today?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "one million"

  Scenario: SQuAD Sample 19 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 19" and content "The region is home to about 2.5 million insect species, tens of thousands of plants, and some 2,000 birds and mammals. To date, at least 40,000 plant species, 2,200 fishes, 1,294 birds, 427 mammals, 428 amphibians, and 378 reptiles have been scientifically classified in the region. One in five of all the bird species in the world live in the rainforests of the Amazon, and one in five of the fish species live in Amazonian rivers and streams. Scientists have described between 96,660 and 128,843 invertebrate species in Brazil alone."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 19 Chat"
    When I send a message with content "The Amazon region is home to how many species of insect?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "2.5 million"

  Scenario: SQuAD Sample 20 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 20" and content "Courts have distinguished between two types of civil disobedience: \"Indirect civil disobedience involves violating a law which is not, itself, the object of protest, whereas direct civil disobedience involves protesting the existence of a particular law by breaking that law.\" During the Vietnam War, courts typically refused to excuse the perpetrators of illegal protests from punishment on the basis of their challenging the legality of the Vietnam War; the courts ruled it was a political question. The necessity defense has sometimes been used as a shadow defense by civil disobedients to deny guilt without denouncing their politically motivated acts, and to present their political beliefs in the courtroom. However, court cases such as U.S. v. Schoon have greatly curtailed the availability of the political necessity defense. Likewise, when Carter Wentworth was charged for his role in the Clamshell Alliance's 1977 illegal occupation of the Seabrook Station Nuclear Power Plant, the judge instructed the jury to disregard his competing harms defense, and he was found guilty. Fully Informed Jury Association activists have sometimes handed out educational leaflets inside courthouses despite admonitions not to; according to FIJA, many of them have escaped prosecution because \"prosecutors have reasoned (correctly) that if they arrest fully informed jury leafleters, the leaflets will have to be given to the leafleter's own jury as evidence.\""
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 20 Chat"
    When I send a message with content "Who passed out educational leaflets in courtrooms during the Vietnam War?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 21 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 21" and content "The plague repeatedly returned to haunt Europe and the Mediterranean throughout the 14th to 17th centuries. According to Biraben, the plague was present somewhere in Europe in every year between 1346 and 1671. The Second Pandemic was particularly widespread in the following years: 1360–63; 1374; 1400; 1438–39; 1456–57; 1464–66; 1481–85; 1500–03; 1518–31; 1544–48; 1563–66; 1573–88; 1596–99; 1602–11; 1623–40; 1644–54; and 1664–67. Subsequent outbreaks, though severe, marked the retreat from most of Europe (18th century) and northern Africa (19th century). According to Geoffrey Parker, \"France alone lost almost a million people to the plague in the epidemic of 1628–31.\""
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 21 Chat"
    When I send a message with content "What is Biraben's first name?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 22 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 22" and content "On August 15, 1971, the United States unilaterally pulled out of the Bretton Woods Accord. The US abandoned the Gold Exchange Standard whereby the value of the dollar had been pegged to the price of gold and all other currencies were pegged to the dollar, whose value was left to \"float\" (rise and fall according to market demand). Shortly thereafter, Britain followed, floating the pound sterling. The other industrialized nations followed suit with their respective currencies. Anticipating that currency values would fluctuate unpredictably for a time, the industrialized nations increased their reserves (by expanding their money supplies) in amounts far greater than before. The result was a depreciation of the dollar and other industrialized nations' currencies. Because oil was priced in dollars, oil producers' real income decreased. In September 1971, OPEC issued a joint communiqué stating that, from then on, they would price oil in terms of a fixed amount of gold."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 22 Chat"
    When I send a message with content "In what year did OPEC pull out of the Bretton Woods Accord?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 23 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 23" and content "The study also found that there were two previously unknown but related clades (genetic branches) of the Y. pestis genome associated with medieval mass graves. These clades (which are thought to be extinct) were found to be ancestral to modern isolates of the modern Y. pestis strains Y. p. orientalis and Y. p. medievalis, suggesting the plague may have entered Europe in two waves. Surveys of plague pit remains in France and England indicate the first variant entered Europe through the port of Marseille around November 1347 and spread through France over the next two years, eventually reaching England in the spring of 1349, where it spread through the country in three epidemics. Surveys of plague pit remains from the Dutch town of Bergen op Zoom showed the Y. pestis genotype responsible for the pandemic that spread through the Low Countries from 1350 differed from that found in Britain and France, implying Bergen op Zoom (and possibly other parts of the southern Netherlands) was not directly infected from England or France in 1349 and suggesting a second wave of plague, different from those in Britain and France, may have been carried to the Low Countries from Norway, the Hanseatic cities or another site."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 23 Chat"
    When I send a message with content "What was one of the Hanseatic cities?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 24 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 24" and content "Much of the work of the Scottish Parliament is done in committee. The role of committees is stronger in the Scottish Parliament than in other parliamentary systems, partly as a means of strengthening the role of backbenchers in their scrutiny of the government and partly to compensate for the fact that there is no revising chamber. The principal role of committees in the Scottish Parliament is to take evidence from witnesses, conduct inquiries and scrutinise legislation. Committee meetings take place on Tuesday, Wednesday and Thursday morning when Parliament is sitting. Committees can also meet at other locations throughout Scotland."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 24 Chat"
    When I send a message with content "Where is much of the work of the Scottish Parliament done?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "committee"

  Scenario: SQuAD Sample 25 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 25" and content "The variant forms of the name of the Rhine in modern languages are all derived from the Gaulish name Rēnos, which was adapted in Roman-era geography (1st century BC) as Greek Ῥῆνος (Rhēnos), Latin Rhenus.[note 3] The spelling with Rh- in English Rhine as well as in German Rhein and French Rhin is due to the influence of Greek orthography, while the vocalisation -i- is due to the Proto-Germanic adoption of the Gaulish name as *Rīnaz, via Old Frankish giving Old English Rín, Old High German Rīn, Dutch Rijn (formerly also spelled Rhijn)). The diphthong in modern German Rhein (also adopted in Romansh Rein, Rain) is a Central German development of the early modern period, the Alemannic name Rī(n) retaining the older vocalism,[note 4] as does Ripuarian Rhing, while Palatine has diphthongized Rhei, Rhoi. Spanish is with French in adopting the Germanic vocalism Rin-, while Italian, Occitan and Portuguese retain the Latin Ren-."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 25 Chat"
    When I send a message with content "How was the Dutch name for the Rhine originally spelled? "
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Rhijn"

  Scenario: SQuAD Sample 26 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 26" and content "The length of the Rhine is conventionally measured in \"Rhine-kilometers\" (Rheinkilometer), a scale introduced in 1939 which runs from the Old Rhine Bridge at Constance (0 km) to Hoek van Holland (1036.20 km). The river length is significantly shortened from the river's natural course due to number of canalisation projects completed in the 19th and 20th century.[note 7] The \"total length of the Rhine\", to the inclusion of Lake Constance and the Alpine Rhine is more difficult to measure objectively; it was cited as 1,232 kilometres (766 miles) by the Dutch Rijkswaterstaat in 2010.[note 1]"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 26 Chat"
    When I send a message with content "Where does the Rhine river's measurement begin?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Old Rhine Bridge at Constance"

  Scenario: SQuAD Sample 27 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 27" and content "Many complexity classes are defined using the concept of a reduction. A reduction is a transformation of one problem into another problem. It captures the informal notion of a problem being at least as difficult as another problem. For instance, if a problem X can be solved using an algorithm for Y, X is no more difficult than Y, and we say that X reduces to Y. There are many different types of reductions, based on the method of reduction, such as Cook reductions, Karp reductions and Levin reductions, and the bound on the complexity of reductions, such as polynomial-time reductions or log-space reductions."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 27 Chat"
    When I send a message with content "According to reduction, if X and Y can be solved by the same algorithm then X performs what function in relationship to Y?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "reduces"

  Scenario: SQuAD Sample 28 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 28" and content "Telenet was the first FCC-licensed public data network in the United States. It was founded by former ARPA IPTO director Larry Roberts as a means of making ARPANET technology public. He had tried to interest AT&T in buying the technology, but the monopoly's reaction was that this was incompatible with their future. Bolt, Beranack and Newman (BBN) provided the financing. It initially used ARPANET technology but changed the host interface to X.25 and the terminal interface to X.29. Telenet designed these protocols and helped standardize them in the CCITT. Telenet was incorporated in 1973 and started operations in 1975. It went public in 1979 and was then sold to GTE."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 28 Chat"
    When I send a message with content "Telnet was sold to "
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Telenet was incorporated in 1973 and started operations in 1975. It went public in 1979 and was then sold to GTE"

  Scenario: SQuAD Sample 29 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 29" and content "AppleTalk was a proprietary suite of networking protocols developed by Apple Inc. in 1985 for Apple Macintosh computers. It was the primary protocol used by Apple devices through the 1980s and 90s. AppleTalk included features that allowed local area networks to be established ad hoc without the requirement for a centralized router or server. The AppleTalk system automatically assigned addresses, updated the distributed namespace, and configured any required inter-network routing. It was a plug-n-play system."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 29 Chat"
    When I send a message with content "What was Apple Talk "
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "a proprietary suite of networking protocols developed by Apple Inc. in 1985"

  Scenario: SQuAD Sample 30 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 30" and content "In 1900, the Los Angeles Times defined southern California as including \"the seven counties of Los Angeles, San Bernardino, Orange, Riverside, San Diego, Ventura and Santa Barbara.\" In 1999, the Times added a newer county—Imperial—to that list."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 30 Chat"
    When I send a message with content "How many counties initially made up the definition of southern California?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "seven"

  Scenario: SQuAD Sample 31 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 31" and content "Another example of scientific research which suggests that previous estimates by the IPCC, far from overstating dangers and risks, have actually understated them is a study on projected rises in sea levels. When the researchers' analysis was \"applied to the possible scenarios outlined by the Intergovernmental Panel on Climate Change (IPCC), the researchers found that in 2100 sea levels would be 0.5–1.4 m [50–140 cm] above 1990 levels. These values are much greater than the 9–88 cm as projected by the IPCC itself in its Third Assessment Report, published in 2001\". This may have been due, in part, to the expanding human understanding of climate."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 31 Chat"
    When I send a message with content "Which study suggests that previous estimates were overstated?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 32 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 32" and content "Development of the fertilized eggs is direct, in other words there is no distinctive larval form, and juveniles of all groups generally resemble miniature cydippid adults. In the genus Beroe the juveniles, like the adults, lack tentacles and tentacle sheaths. In most species the juveniles gradually develop the body forms of their parents. In some groups, such as the flat, bottom-dwelling platyctenids, the juveniles behave more like true larvae, as they live among the plankton and thus occupy a different ecological niche from their parents and attain the adult form by a more radical metamorphosis, after dropping to the sea-floor."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 32 Chat"
    When I send a message with content "What kind of area do the genus Beroe juveniles live in that's different than their parents?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 33 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 33" and content "Normans came into Scotland, building castles and founding noble families who would provide some future kings, such as Robert the Bruce, as well as founding a considerable number of the Scottish clans. King David I of Scotland, whose elder brother Alexander I had married Sybilla of Normandy, was instrumental in introducing Normans and Norman culture to Scotland, part of the process some scholars call the \"Davidian Revolution\". Having spent time at the court of Henry I of England (married to David's sister Maud of Scotland), and needing them to wrestle the kingdom from his half-brother Máel Coluim mac Alaxandair, David had to reward many with lands. The process was continued under David's successors, most intensely of all under William the Lion. The Norman-derived feudal system was applied in varying degrees to most of Scotland. Scottish families of the names Bruce, Gray, Ramsay, Fraser, Ogilvie, Montgomery, Sinclair, Pollock, Burnard, Douglas and Gordon to name but a few, and including the later royal House of Stewart, can all be traced back to Norman ancestry."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 33 Chat"
    When I send a message with content "Who did Alexander I marry?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Sybilla of Normandy"

  Scenario: SQuAD Sample 34 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 34" and content "From the death of Augustus in AD 14 until after AD 70, Rome accepted as her Germanic frontier the water-boundary of the Rhine and upper Danube. Beyond these rivers she held only the fertile plain of Frankfurt, opposite the Roman border fortress of Moguntiacum (Mainz), the southernmost slopes of the Black Forest and a few scattered bridge-heads. The northern section of this frontier, where the Rhine is deep and broad, remained the Roman boundary until the empire fell. The southern part was different. The upper Rhine and upper Danube are easily crossed. The frontier which they form is inconveniently long, enclosing an acute-angled wedge of foreign territory between the modern Baden and Württemberg. The Germanic populations of these lands seem in Roman times to have been scanty, and Roman subjects from the modern Alsace-Lorraine had drifted across the river eastwards."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 34 Chat"
    When I send a message with content "What populations occupied the foreign territory between the modern Baden and Württemberg?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 35 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 35" and content "The official record high temperature for Fresno is 115 °F (46.1 °C), set on July 8, 1905, while the official record low is 17 °F (−8 °C), set on January 6, 1913. The average windows for 100 °F (37.8 °C)+, 90 °F (32.2 °C)+, and freezing temperatures are June 1 thru September 13, April 26 thru October 9, and December 10 thru January 28, respectively, and no freeze occurred between in the 1983/1984 season. Annual rainfall has ranged from 23.57 inches (598.7 mm) in the “rain year” from July 1982 to June 1983 down to 4.43 inches (112.5 mm) from July 1933 to June 1934. The most rainfall in one month was 9.54 inches (242.3 mm) in November 1885 and the most rainfall in 24 hours 3.55 inches (90.2 mm) on November 18, 1885. Measurable precipitation falls on an average of 48 days annually. Snow is a rarity; the heaviest snowfall at the airport was 2.2 inches (0.06 m) on January 21, 1962."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 35 Chat"
    When I send a message with content "What is the hottest temperature record for Fresno?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "115 °F"

  Scenario: SQuAD Sample 36 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 36" and content "The main use for steam turbines is in electricity generation (in the 1990s about 90% of the world's electric production was by use of steam turbines) however the recent widespread application of large gas turbine units and typical combined cycle power plants has resulted in reduction of this percentage to the 80% regime for steam turbines. In electricity production, the high speed of turbine rotation matches well with the speed of modern electric generators, which are typically direct connected to their driving turbines. In marine service, (pioneered on the Turbinia), steam turbines with reduction gearing (although the Turbinia has direct turbines to propellers with no reduction gearbox) dominated large ship propulsion throughout the late 20th century, being more efficient (and requiring far less maintenance) than reciprocating steam engines. In recent decades, reciprocating Diesel engines, and gas turbines, have almost entirely supplanted steam propulsion for marine applications."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 36 Chat"
    When I send a message with content "What gearing was used on steam turbine engines until the 1990s?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 37 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 37" and content "The Social Chapter is a chapter of the 1997 Treaty of Amsterdam covering social policy issues in European Union law. The basis for the Social Chapter was developed in 1989 by the \"social partners\" representatives, namely UNICE, the employers' confederation, the European Trade Union Confederation (ETUC) and CEEP, the European Centre of Public Enterprises. A toned down version was adopted as the Social Charter at the 1989 Strasbourg European Council. The Social Charter declares 30 general principles, including on fair remuneration of employment, health and safety at work, rights of disabled and elderly, the rights of workers, on vocational training and improvements of living conditions. The Social Charter became the basis for European Community legislation on these issues in 40 pieces of legislation."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 37 Chat"
    When I send a message with content "What treaty is the Social Chapter not a chapter of?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 38 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 38" and content "Sayyid Abul Ala Maududi was an important early twentieth-century figure in the Islamic revival in India, and then after independence from Britain, in Pakistan. Trained as a lawyer he chose the profession of journalism, and wrote about contemporary issues and most importantly about Islam and Islamic law. Maududi founded the Jamaat-e-Islami party in 1941 and remained its leader until 1972. However, Maududi had much more impact through his writing than through his political organising. His extremely influential books (translated into many languages) placed Islam in a modern context, and influenced not only conservative ulema but liberal modernizer Islamists such as al-Faruqi, whose \"Islamization of Knowledge\" carried forward some of Maududi's key principles."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 38 Chat"
    When I send a message with content " Where did Maududi's books not place Islam?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 39 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 39" and content "AppleTalk was a proprietary suite of networking protocols developed by Apple Inc. in 1985 for Apple Macintosh computers. It was the primary protocol used by Apple devices through the 1980s and 90s. AppleTalk included features that allowed local area networks to be established ad hoc without the requirement for a centralized router or server. The AppleTalk system automatically assigned addresses, updated the distributed namespace, and configured any required inter-network routing. It was a plug-n-play system."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 39 Chat"
    When I send a message with content "What created a centralized router or server?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 40 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 40" and content "Before the foundation can be dug, contractors are typically required to verify and have existing utility lines marked, either by the utilities themselves or through a company specializing in such services. This lessens the likelihood of damage to the existing electrical, water, sewage, phone, and cable facilities, which could cause outages and potentially hazardous situations. During the construction of a building, the municipal building inspector inspects the building periodically to ensure that the construction adheres to the approved plans and the local building code. Once construction is complete and a final inspection has been passed, an occupancy permit may be issued."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 40 Chat"
    When I send a message with content "What are some existing facilities?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "electrical, water, sewage, phone, and cable facilities"

  Scenario: SQuAD Sample 41 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 41" and content "The Lower Rhine flows through North Rhine-Westphalia. Its banks are usually heavily populated and industrialized, in particular the agglomerations Cologne, Düsseldorf and Ruhr area. Here the Rhine flows through the largest conurbation in Germany, the Rhine-Ruhr region. One of the most important cities in this region is Duisburg with the largest river port in Europe (Duisport). The region downstream of Duisburg is more agricultural. In Wesel, 30 km downstream of Duisburg, is located the western end of the second east-west shipping route, the Wesel-Datteln Canal, which runs parallel to the Lippe. Between Emmerich and Cleves the Emmerich Rhine Bridge, the longest suspension bridge in Germany, crosses the 400 m wide river. Near Krefeld, the river crosses the Uerdingen line, the line which separates the areas where Low German and High German are spoken."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 41 Chat"
    When I send a message with content "What part of the Rhine flows through North Rhine-Westphalia?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Lower Rhine"

  Scenario: SQuAD Sample 42 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 42" and content "When Céloron's expedition arrived at Logstown, the Native Americans in the area informed Céloron that they owned the Ohio Country and that they would trade with the British regardless of the French. Céloron continued south until his expedition reached the confluence of the Ohio and the Miami rivers, which lay just south of the village of Pickawillany, the home of the Miami chief known as \"Old Briton\". Céloron threatened \"Old Briton\" with severe consequences if he continued to trade with the British. \"Old Briton\" ignored the warning. Disappointed, Céloron returned to Montreal in November 1749."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 42 Chat"
    When I send a message with content "How did Celeron handle meeting with New Briton?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 43 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 43" and content "Fresno (/ˈfrɛznoʊ/ FREZ-noh), the county seat of Fresno County, is a city in the U.S. state of California. As of 2015, the city's population was 520,159, making it the fifth-largest city in California, the largest inland city in California and the 34th-largest in the nation. Fresno is in the center of the San Joaquin Valley and is the largest city in the Central Valley, which contains the San Joaquin Valley. It is approximately 220 miles (350 km) northwest of Los Angeles, 170 miles (270 km) south of the state capital, Sacramento, or 185 miles (300 km) south of San Francisco. The name Fresno means \"ash tree\" in Spanish, and an ash leaf is featured on the city's flag."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 43 Chat"
    When I send a message with content "What is the population of Los Angeles?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 44 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 44" and content "In literature, author of the New York Times bestseller Before I Fall Lauren Oliver, Pulitzer Prize winning novelist Philip Roth, Canadian-born Pulitzer Prize and Nobel Prize for Literature winning writer Saul Bellow, political philosopher, literary critic and author of the New York Times bestseller \"The Closing of the American Mind\" Allan Bloom, ''The Good War\" author Studs Terkel, American writer, essayist, filmmaker, teacher, and political activist Susan Sontag, analytic philosopher and Stanford University Professor of Comparative Literature Richard Rorty, and American writer and satirist Kurt Vonnegut are notable alumni."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 44 Chat"
    When I send a message with content "Who wrote the American Times bestselling book titled \"The Closing of the American Mind\"?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 45 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 45" and content "Islamism is a controversial concept not just because it posits a political role for Islam but also because its supporters believe their views merely reflect Islam, while the contrary idea that Islam is, or can be, apolitical is an error. Scholars and observers who do not believe that Islam is merely a political ideology include Fred Halliday, John Esposito and Muslim intellectuals like Javed Ahmad Ghamidi. Hayri Abaza argues the failure to distinguish between Islam and Islamism leads many in the West to support illiberal Islamic regimes, to the detriment of progressive moderates who seek to separate religion from politics."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 45 Chat"
    When I send a message with content "The idea that Islam can be apolitical isn't able to be embraced by whom?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "its supporters"

  Scenario: SQuAD Sample 46 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 46" and content "The variant forms of the name of the Rhine in modern languages are all derived from the Gaulish name Rēnos, which was adapted in Roman-era geography (1st century BC) as Greek Ῥῆνος (Rhēnos), Latin Rhenus.[note 3] The spelling with Rh- in English Rhine as well as in German Rhein and French Rhin is due to the influence of Greek orthography, while the vocalisation -i- is due to the Proto-Germanic adoption of the Gaulish name as *Rīnaz, via Old Frankish giving Old English Rín, Old High German Rīn, Dutch Rijn (formerly also spelled Rhijn)). The diphthong in modern German Rhein (also adopted in Romansh Rein, Rain) is a Central German development of the early modern period, the Alemannic name Rī(n) retaining the older vocalism,[note 4] as does Ripuarian Rhing, while Palatine has diphthongized Rhei, Rhoi. Spanish is with French in adopting the Germanic vocalism Rin-, while Italian, Occitan and Portuguese retain the Latin Ren-."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 46 Chat"
    When I send a message with content "What century did the Germanic vocalism Rin come from?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 47 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 47" and content "Before the foundation can be dug, contractors are typically required to verify and have existing utility lines marked, either by the utilities themselves or through a company specializing in such services. This lessens the likelihood of damage to the existing electrical, water, sewage, phone, and cable facilities, which could cause outages and potentially hazardous situations. During the construction of a building, the municipal building inspector inspects the building periodically to ensure that the construction adheres to the approved plans and the local building code. Once construction is complete and a final inspection has been passed, an occupancy permit may be issued."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 47 Chat"
    When I send a message with content "What happens before the foundation is dug and when a final inspection is passed?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 48 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 48" and content "The Standard Industrial Classification and the newer North American Industry Classification System have a classification system for companies that perform or otherwise engage in construction. To recognize the differences of companies in this sector, it is divided into three subsectors: building construction, heavy and civil engineering construction, and specialty trade contractors. There are also categories for construction service firms (e.g., engineering, architecture) and construction managers (firms engaged in managing construction projects without assuming direct financial responsibility for completion of the construction project)."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 48 Chat"
    When I send a message with content "What does heavy and civil engineering construction not do when managing projects?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 49 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 49" and content "France took control of Algeria in 1830 but began in earnest to rebuild its worldwide empire after 1850, concentrating chiefly in North and West Africa, as well as South-East Asia, with other conquests in Central and East Africa, as well as the South Pacific. Republicans, at first hostile to empire, only became supportive when Germany started to build her own colonial empire. As it developed, the new empire took on roles of trade with France, supplying raw materials and purchasing manufactured items, as well as lending prestige to the motherland and spreading French civilization and language as well as Catholicism. It also provided crucial manpower in both World Wars."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 49 Chat"
    When I send a message with content "Where did France focus its efforts to rebuild its empire?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Africa"

  Scenario: SQuAD Sample 50 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 50" and content "British researchers Richard G. Wilkinson and Kate Pickett have found higher rates of health and social problems (obesity, mental illness, homicides, teenage births, incarceration, child conflict, drug use), and lower rates of social goods (life expectancy by country, educational performance, trust among strangers, women's status, social mobility, even numbers of patents issued) in countries and states with higher inequality. Using statistics from 23 developed countries and the 50 states of the US, they found social/health problems lower in countries like Japan and Finland and states like Utah and New Hampshire with high levels of equality, than in countries (US and UK) and states (Mississippi and New York) with large differences in household income."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 50 Chat"
    When I send a message with content "Health problems were lower in places with higher levels of what?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "equality"

  Scenario: SQuAD Sample 51 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 51" and content "For a long time, it was thought that the Amazon rainforest was only ever sparsely populated, as it was impossible to sustain a large population through agriculture given the poor soil. Archeologist Betty Meggers was a prominent proponent of this idea, as described in her book Amazonia: Man and Culture in a Counterfeit Paradise. She claimed that a population density of 0.2 inhabitants per square kilometre (0.52/sq mi) is the maximum that can be sustained in the rainforest through hunting, with agriculture needed to host a larger population. However, recent anthropological findings have suggested that the region was actually densely populated. Some 5 million people may have lived in the Amazon region in AD 1500, divided between dense coastal settlements, such as that at Marajó, and inland dwellers. By 1900 the population had fallen to 1 million and by the early 1980s it was less than 200,000."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 51 Chat"
    When I send a message with content "What would be needed to host a larger population?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "agriculture"

  Scenario: SQuAD Sample 52 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 52" and content "The modern trend in design is toward integration of previously separated specialties, especially among large firms. In the past, architects, interior designers, engineers, developers, construction managers, and general contractors were more likely to be entirely separate companies, even in the larger firms. Presently, a firm that is nominally an \"architecture\" or \"construction management\" firm may have experts from all related fields as employees, or to have an associated company that provides each necessary skill. Thus, each such firm may offer itself as \"one-stop shopping\" for a construction project, from beginning to end. This is designated as a \"design build\" contract where the contractor is given a performance specification and must undertake the project from design to construction, while adhering to the performance specifications."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 52 Chat"
    When I send a message with content "What types of employees does and interior design firm usually have?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 53 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 53" and content "The Iroquois sent runners to the manor of William Johnson in upstate New York. The British Superintendent for Indian Affairs in the New York region and beyond, Johnson was known to the Iroquois as Warraghiggey, meaning \"He who does great things.\" He spoke their languages and had become a respected honorary member of the Iroquois Confederacy in the area. In 1746, Johnson was made a colonel of the Iroquois. Later he was commissioned as a colonel of the Western New York Militia. They met at Albany, New York with Governor Clinton and officials from some of the other American colonies. Mohawk Chief Hendrick, Speaker of their tribal council, insisted that the British abide by their obligations and block French expansion. When Clinton did not respond to his satisfaction, Chief Hendrick said that the \"Covenant Chain\", a long-standing friendly relationship between the Iroquois Confederacy and the British Crown, was broken."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 53 Chat"
    When I send a message with content "What was William Johnson's Sioux name?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 54 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 54" and content "A controversial aspect of imperialism is the defense and justification of empire-building based on seemingly rational grounds. J. A. Hobson identifies this justification on general grounds as: \"It is desirable that the earth should be peopled, governed, and developed, as far as possible, by the races which can do this work best, i.e. by the races of highest 'social efficiency'\". Many others argued that imperialism is justified for several different reasons. Friedrich Ratzel believed that in order for a state to survive, imperialism was needed. Halford Mackinder felt that Great Britain needed to be one of the greatest imperialists and therefore justified imperialism. The purportedly scientific nature of \"Social Darwinism\" and a theory of races formed a supposedly rational justification for imperialism. The rhetoric of colonizers being racially superior appears to have achieved its purpose, for example throughout Latin America \"whiteness\" is still prized today and various forms of blanqueamiento (whitening) are common."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 54 Chat"
    When I send a message with content "what is the least controversial aspect of imperialism?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 55 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 55" and content "The concept of prime number is so important that it has been generalized in different ways in various branches of mathematics. Generally, \"prime\" indicates minimality or indecomposability, in an appropriate sense. For example, the prime field is the smallest subfield of a field F containing both 0 and 1. It is either Q or the finite field with p elements, whence the name. Often a second, additional meaning is intended by using the word prime, namely that any object can be, essentially uniquely, decomposed into its prime components. For example, in knot theory, a prime knot is a knot that is indecomposable in the sense that it cannot be written as the knot sum of two nontrivial knots. Any knot can be uniquely expressed as a connected sum of prime knots. Prime models and prime 3-manifolds are other examples of this type."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 55 Chat"
    When I send a message with content "For a field F containing 0 and 1, what would be the prime knot field?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 56 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 56" and content "The first historical reference to Warsaw dates back to the year 1313, at a time when Kraków served as the Polish capital city. Due to its central location between the Polish–Lithuanian Commonwealth's capitals of Kraków and Vilnius, Warsaw became the capital of the Commonwealth and of the Crown of the Kingdom of Poland when King Sigismund III Vasa moved his court from Kraków to Warsaw in 1596. After the Third Partition of Poland in 1795, Warsaw was incorporated into the Kingdom of Prussia. In 1806 during the Napoleonic Wars, the city became the official capital of the Grand Duchy of Warsaw, a puppet state of the First French Empire established by Napoleon Bonaparte. In accordance with the decisions of the Congress of Vienna, the Russian Empire annexed Warsaw in 1815 and it became part of the \"Congress Kingdom\". Only in 1918 did it regain independence from the foreign rule and emerge as a new capital of the independent Republic of Poland. The German invasion in 1939, the massacre of the Jewish population and deportations to concentration camps led to the uprising in the Warsaw ghetto in 1943 and to the major and devastating Warsaw Uprising between August and October 1944. Warsaw gained the title of the \"Phoenix City\" because it has survived many wars, conflicts and invasions throughout its long history. Most notably, the city required painstaking rebuilding after the extensive damage it suffered in World War II, which destroyed 85% of its buildings. On 9 November 1940, the city was awarded Poland's highest military decoration for heroism, the Virtuti Militari, during the Siege of Warsaw (1939)."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 56 Chat"
    When I send a message with content "What city served as Poland's capital in 1313?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Kraków"

  Scenario: SQuAD Sample 57 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 57" and content "In World War II, Charles de Gaulle and the Free French used the overseas colonies as bases from which they fought to liberate France. However after 1945 anti-colonial movements began to challenge the Empire. France fought and lost a bitter war in Vietnam in the 1950s. Whereas they won the war in Algeria, the French leader at the time, Charles de Gaulle, decided to grant Algeria independence anyway in 1962. Its settlers and many local supporters relocated to France. Nearly all of France's colonies gained independence by 1960, but France retained great financial and diplomatic influence. It has repeatedly sent troops to assist its former colonies in Africa in suppressing insurrections and coups d’état."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 57 Chat"
    When I send a message with content " After 1945, what challenged the British empire?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 58 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 58" and content "Singlet oxygen is a name given to several higher-energy species of molecular O 2 in which all the electron spins are paired. It is much more reactive towards common organic molecules than is molecular oxygen per se. In nature, singlet oxygen is commonly formed from water during photosynthesis, using the energy of sunlight. It is also produced in the troposphere by the photolysis of ozone by light of short wavelength, and by the immune system as a source of active oxygen. Carotenoids in photosynthetic organisms (and possibly also in animals) play a major role in absorbing energy from singlet oxygen and converting it to the unexcited ground state before it can cause harm to tissues."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 58 Chat"
    When I send a message with content "By what process is singlet oxygen made in the tropophere?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "photolysis of ozone"

  Scenario: SQuAD Sample 59 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 59" and content "Europe's expansion into territorial imperialism was largely focused on economic growth by collecting resources from colonies, in combination with assuming political control by military and political means. The colonization of India in the mid-18th century offers an example of this focus: there, the \"British exploited the political weakness of the Mughal state, and, while military activity was important at various times, the economic and administrative incorporation of local elites was also of crucial significance\" for the establishment of control over the subcontinent's resources, markets, and manpower. Although a substantial number of colonies had been designed to provide economic profit and to ship resources to home ports in the seventeenth and eighteenth centuries, Fieldhouse suggests that in the nineteenth and twentieth centuries in places such as Africa and Asia, this idea is not necessarily valid:"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 59 Chat"
    When I send a message with content " What was made valid in the late 19th and 20th centuries?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 60 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 60" and content "The Harvard Business School and many of the university's athletics facilities, including Harvard Stadium, are located on a 358-acre (145 ha) campus opposite the Cambridge campus in Allston. The John W. Weeks Bridge is a pedestrian bridge over the Charles River connecting both campuses. The Harvard Medical School, Harvard School of Dental Medicine, and the Harvard School of Public Health are located on a 21-acre (8.5 ha) campus in the Longwood Medical and Academic Area approximately 3.3 miles (5.3 km) southwest of downtown Boston and 3.3 miles (5.3 km) south of the Cambridge campus."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 60 Chat"
    When I send a message with content "Where are the Harvard medical, Dental and school of Public Health located?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Longwood Medical and Academic Area"

  Scenario: SQuAD Sample 61 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 61" and content "The first historical reference to Warsaw dates back to the year 1313, at a time when Kraków served as the Polish capital city. Due to its central location between the Polish–Lithuanian Commonwealth's capitals of Kraków and Vilnius, Warsaw became the capital of the Commonwealth and of the Crown of the Kingdom of Poland when King Sigismund III Vasa moved his court from Kraków to Warsaw in 1596. After the Third Partition of Poland in 1795, Warsaw was incorporated into the Kingdom of Prussia. In 1806 during the Napoleonic Wars, the city became the official capital of the Grand Duchy of Warsaw, a puppet state of the First French Empire established by Napoleon Bonaparte. In accordance with the decisions of the Congress of Vienna, the Russian Empire annexed Warsaw in 1815 and it became part of the \"Congress Kingdom\". Only in 1918 did it regain independence from the foreign rule and emerge as a new capital of the independent Republic of Poland. The German invasion in 1939, the massacre of the Jewish population and deportations to concentration camps led to the uprising in the Warsaw ghetto in 1943 and to the major and devastating Warsaw Uprising between August and October 1944. Warsaw gained the title of the \"Phoenix City\" because it has survived many wars, conflicts and invasions throughout its long history. Most notably, the city required painstaking rebuilding after the extensive damage it suffered in World War II, which destroyed 85% of its buildings. On 9 November 1940, the city was awarded Poland's highest military decoration for heroism, the Virtuti Militari, during the Siege of Warsaw (1939)."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 61 Chat"
    When I send a message with content "When did Warsaw become the capital of the Kingdom of Prussia?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 62 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 62" and content "A term used originally in derision, Huguenot has unclear origins. Various hypotheses have been promoted. The nickname may have been a combined reference to the Swiss politician Besançon Hugues (died 1532) and the religiously conflicted nature of Swiss republicanism in his time, using a clever derogatory pun on the name Hugues by way of the Dutch word Huisgenoten (literally housemates), referring to the connotations of a somewhat related word in German Eidgenosse (Confederates as in \"a citizen of one of the states of the Swiss Confederacy\"). Geneva was John Calvin's adopted home and the centre of the Calvinist movement. In Geneva, Hugues, though Catholic, was a leader of the \"Confederate Party\", so called because it favoured independence from the Duke of Savoy through an alliance between the city-state of Geneva and the Swiss Confederation. The label Huguenot was purportedly first applied in France to those conspirators (all of them aristocratic members of the Reformed Church) involved in the Amboise plot of 1560: a foiled attempt to wrest power in France from the influential House of Guise. The move would have had the side effect of fostering relations with the Swiss. Thus, Hugues plus Eidgenosse by way of Huisgenoten supposedly became Huguenot, a nickname associating the Protestant cause with politics unpopular in France.[citation needed]"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 62 Chat"
    When I send a message with content "What Swiss city was the center of the Calvinist movement?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Geneva"

  Scenario: SQuAD Sample 63 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 63" and content "In 1973, Nixon named William E. Simon as the first Administrator of the Federal Energy Office, a short-term organization created to coordinate the response to the embargo. Simon allocated states the same amount of domestic oil for 1974 that each had consumed in 1972, which worked for states whose populations were not increasing. In other states, lines at gasoline stations were common. The American Automobile Association reported that in the last week of February 1974, 20% of American gasoline stations had no fuel."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 63 Chat"
    When I send a message with content "What percentage of American gas stations were out of fuel in 1973?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 64 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 64" and content "Islamism, also known as Political Islam (Arabic: إسلام سياسي‎ islām siyāsī), is an Islamic revival movement often characterized by moral conservatism, literalism, and the attempt \"to implement Islamic values in all spheres of life.\" Islamism favors the reordering of government and society in accordance with the Shari'a. The different Islamist movements have been described as \"oscillating between two poles\": at one end is a strategy of Islamization of society through state power seized by revolution or invasion; at the other \"reformist\" pole Islamists work to Islamize society gradually \"from the bottom up\". The movements have \"arguably altered the Middle East more than any trend since the modern states gained independence\", redefining \"politics and even borders\" according to one journalist (Robin Wright)."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 64 Chat"
    When I send a message with content "What have the two different Islamist movements been described as oscillating between?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "poles"

  Scenario: SQuAD Sample 65 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 65" and content "The graph isomorphism problem is the computational problem of determining whether two finite graphs are isomorphic. An important unsolved problem in complexity theory is whether the graph isomorphism problem is in P, NP-complete, or NP-intermediate. The answer is not known, but it is believed that the problem is at least not NP-complete. If graph isomorphism is NP-complete, the polynomial time hierarchy collapses to its second level. Since it is widely believed that the polynomial hierarchy does not collapse to any finite level, it is believed that graph isomorphism is not NP-complete. The best algorithm for this problem, due to Laszlo Babai and Eugene Luks has run time 2O(√(n log(n))) for graphs with n vertices."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 65 Chat"
    When I send a message with content "What is the problem attributed to defining if two finite graphs are isomorphic?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "The graph isomorphism problem"

  Scenario: SQuAD Sample 66 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 66" and content "Oxygen is a chemical element with symbol O and atomic number 8. It is a member of the chalcogen group on the periodic table and is a highly reactive nonmetal and oxidizing agent that readily forms compounds (notably oxides) with most elements. By mass, oxygen is the third-most abundant element in the universe, after hydrogen and helium. At standard temperature and pressure, two atoms of the element bind to form dioxygen, a colorless and odorless diatomic gas with the formula O 2. Diatomic oxygen gas constitutes 20.8% of the Earth's atmosphere. However, monitoring of atmospheric oxygen levels show a global downward trend, because of fossil-fuel burning. Oxygen is the most abundant element by mass in the Earth's crust as part of oxide compounds such as silicon dioxide, making up almost half of the crust's mass."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 66 Chat"
    When I send a message with content "Of what group in the periodic table is oxygen a member?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "chalcogen"

  Scenario: SQuAD Sample 67 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 67" and content "Subject Committees are established at the beginning of each parliamentary session, and again the members on each committee reflect the balance of parties across Parliament. Typically each committee corresponds with one (or more) of the departments (or ministries) of the Scottish Government. The current Subject Committees in the fourth Session are: Economy, Energy and Tourism; Education and Culture; Health and Sport; Justice; Local Government and Regeneration; Rural Affairs, Climate Change and Environment; Welfare Reform; and Infrastructure and Capital Investment."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 67 Chat"
    When I send a message with content "When are subject committees established?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "beginning of each parliamentary session"

  Scenario: SQuAD Sample 68 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 68" and content "Immigrants arrived from all over the world to search for gold, especially from Ireland and China. Many Chinese miners worked in Victoria, and their legacy is particularly strong in Bendigo and its environs. Although there was some racism directed at them, there was not the level of anti-Chinese violence that was seen at the Lambing Flat riots in New South Wales. However, there was a riot at Buckland Valley near Bright in 1857. Conditions on the gold fields were cramped and unsanitary; an outbreak of typhoid at Buckland Valley in 1854 killed over 1,000 miners."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 68 Chat"
    When I send a message with content "Where is the Asian gold miners strongest in Victoria?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 69 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 69" and content "There are 13 natural reserves in Warsaw – among others, Bielany Forest, Kabaty Woods, Czerniaków Lake. About 15 kilometres (9 miles) from Warsaw, the Vistula river's environment changes strikingly and features a perfectly preserved ecosystem, with a habitat of animals that includes the otter, beaver and hundreds of bird species. There are also several lakes in Warsaw – mainly the oxbow lakes, like Czerniaków Lake, the lakes in the Łazienki or Wilanów Parks, Kamionek Lake. There are lot of small lakes in the parks, but only a few are permanent – the majority are emptied before winter to clean them of plants and sediments."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 69 Chat"
    When I send a message with content "What animals does the Czerniakow river's ecosystem include?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 70 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 70" and content "The needs of soy farmers have been used to justify many of the controversial transportation projects that are currently developing in the Amazon. The first two highways successfully opened up the rainforest and led to increased settlement and deforestation. The mean annual deforestation rate from 2000 to 2005 (22,392 km2 or 8,646 sq mi per year) was 18% higher than in the previous five years (19,018 km2 or 7,343 sq mi per year). Although deforestation has declined significantly in the Brazilian Amazon between 2004 and 2014, there has been an increase to the present day."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 70 Chat"
    When I send a message with content "deforestation increased in Brazil during what years?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 71 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 71" and content "The first European to travel the length of the Amazon River was Francisco de Orellana in 1542. The BBC's Unnatural Histories presents evidence that Orellana, rather than exaggerating his claims as previously thought, was correct in his observations that a complex civilization was flourishing along the Amazon in the 1540s. It is believed that the civilization was later devastated by the spread of diseases from Europe, such as smallpox. Since the 1970s, numerous geoglyphs have been discovered on deforested land dating between AD 0–1250, furthering claims about Pre-Columbian civilizations. Ondemar Dias is accredited with first discovering the geoglyphs in 1977 and Alceu Ranzi with furthering their discovery after flying over Acre. The BBC's Unnatural Histories presented evidence that the Amazon rainforest, rather than being a pristine wilderness, has been shaped by man for at least 11,000 years through practices such as forest gardening and terra preta."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 71 Chat"
    When I send a message with content "What was believed to be the cause of devastation to the civilization?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "diseases from Europe"

  Scenario: SQuAD Sample 72 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 72" and content "An important decision for civil disobedients is whether or not to plead guilty. There is much debate on this point, as some believe that it is a civil disobedient's duty to submit to the punishment prescribed by law, while others believe that defending oneself in court will increase the possibility of changing the unjust law. It has also been argued that either choice is compatible with the spirit of civil disobedience. ACT-UP's Civil Disobedience Training handbook states that a civil disobedient who pleads guilty is essentially stating, \"Yes, I committed the act of which you accuse me. I don't deny it; in fact, I am proud of it. I feel I did the right thing by violating this particular law; I am guilty as charged,\" but that pleading not guilty sends a message of, \"Guilt implies wrong-doing. I feel I have done no wrong. I may have violated some specific laws, but I am guilty of doing no wrong. I therefore plead not guilty.\" A plea of no contest is sometimes regarded as a compromise between the two. One defendant accused of illegally protesting nuclear power, when asked to enter his plea, stated, \"I plead for the beauty that surrounds us\"; this is known as a \"creative plea,\" and will usually be interpreted as a plea of not guilty."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 72 Chat"
    When I send a message with content "Which reason is given sometimes to plead not guilty involving these matters?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Guilt implies wrong-doing"

  Scenario: SQuAD Sample 73 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 73" and content "In Ireland, private schools (Irish: scoil phríobháideach) are unusual because a certain number of teacher's salaries are paid by the State. If the school wishes to employ extra teachers they are paid for with school fees, which tend to be relatively low in Ireland compared to the rest of the world. There is, however, a limited element of state assessment of private schools, because of the requirement that the state ensure that children receive a certain minimum education; Irish private schools must still work towards the Junior Certificate and the Leaving Certificate, for example. Many private schools in Ireland also double as boarding schools. The average fee is around €5,000 annually for most schools, but some of these schools also provide boarding and the fees may then rise up to €25,000 per year. The fee-paying schools are usually run by a religious order, i.e., the Society of Jesus or Congregation of Christian Brothers, etc."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 73 Chat"
    When I send a message with content "What certificates must private schools worldwide work towards?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 74 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 74" and content "The Victorian Alps in the northeast are the coldest part of Victoria. The Alps are part of the Great Dividing Range mountain system extending east-west through the centre of Victoria. Average temperatures are less than 9 °C (48 °F) in winter and below 0 °C (32 °F) in the highest parts of the ranges. The state's lowest minimum temperature of −11.7 °C (10.9 °F) was recorded at Omeo on 13 June 1965, and again at Falls Creek on 3 July 1970. Temperature extremes for the state are listed in the table below:"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 74 Chat"
    When I send a message with content "In what direction does the river system extend?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 75 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 75" and content "In anglophone academic works, theories regarding imperialism are often based on the British experience. The term \"Imperialism\" was originally introduced into English in its present sense in the late 1870s by opponents of the allegedly aggressive and ostentatious imperial policies of British prime Minister Benjamin Disraeli. It was shortly appropriated by supporters of \"imperialism\" such as Joseph Chamberlain. For some, imperialism designated a policy of idealism and philanthropy; others alleged that it was characterized by political self-interest, and a growing number associated it with capitalist greed. Liberal John A. Hobson and Marxist Vladimir Lenin added a more theoretical macroeconomic connotation to the term. Lenin in particular exerted substantial influence over later Marxist conceptions of imperialism with his work Imperialism, the Highest Stage of Capitalism. In his writings Lenin portrayed Imperialism as a natural extension of capitalism that arose from need for capitalist economies to constantly expand investment, material resources and manpower in such a way that necessitated colonial expansion. This conception of imperialism as a structural feature of capitalism is echoed by later Marxist theoreticians. Many theoreticians on the left have followed in emphasizing the structural or systemic character of \"imperialism\". Such writers have expanded the time period associated with the term so that it now designates neither a policy, nor a short space of decades in the late 19th century, but a world system extending over a period of centuries, often going back to Christopher Columbus and, in some accounts, to the Crusades. As the application of the term has expanded, its meaning has shifted along five distinct but often parallel axes: the moral, the economic, the systemic, the cultural, and the temporal. Those changes reflect - among other shifts in sensibility - a growing unease, even squeamishness, with the fact of power, specifically, Western power."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 75 Chat"
    When I send a message with content "Theories on imperialism don't use which country as a model?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 76 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 76" and content "Nearby, in Ogród Saski (the Saxon Garden), the Summer Theatre was in operation from 1870 to 1939, and in the inter-war period, the theatre complex also included Momus, Warsaw's first literary cabaret, and Leon Schiller's musical theatre Melodram. The Wojciech Bogusławski Theatre (1922–26), was the best example of \"Polish monumental theatre\". From the mid-1930s, the Great Theatre building housed the Upati Institute of Dramatic Arts – the first state-run academy of dramatic art, with an acting department and a stage directing department."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 76 Chat"
    When I send a message with content "What is the Upati Garden in Polish?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 77 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 77" and content "Politically, Victoria has 37 seats in the Australian House of Representatives and 12 seats in the Australian Senate. At state level, the Parliament of Victoria consists of the Legislative Assembly (the lower house) and the Legislative Council (the upper house). Victoria is currently governed by the Labor Party, with Daniel Andrews the current Premier. The personal representative of the Queen of Australia in the state is the Governor of Victoria, currently Linda Dessau. Local government is concentrated in 79 municipal districts, including 33 cities, although a number of unincorporated areas still exist, which are administered directly by the state."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 77 Chat"
    When I send a message with content "How many seats does Australia have in the House of Representatives?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 78 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 78" and content "After Malaysia's independence in 1957, the government instructed all schools to surrender their properties and be assimilated into the National School system. This caused an uproar among the Chinese and a compromise was achieved in that the schools would instead become \"National Type\" schools. Under such a system, the government is only in charge of the school curriculum and teaching personnel while the lands still belonged to the schools. While Chinese primary schools were allowed to retain Chinese as the medium of instruction, Chinese secondary schools are required to change into English-medium schools. Over 60 schools converted to become National Type schools."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 78 Chat"
    When I send a message with content "What type of schools would they have in China as a compromise after Chinese independence?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 79 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 79" and content "Tymnet was an international data communications network headquartered in San Jose, CA that utilized virtual call packet switched technology and used X.25, SNA/SDLC, BSC and ASCII interfaces to connect host computers (servers)at thousands of large companies, educational institutions, and government agencies. Users typically connected via dial-up connections or dedicated async connections. The business consisted of a large public network that supported dial-up users and a private network business that allowed government agencies and large companies (mostly banks and airlines) to build their own dedicated networks. The private networks were often connected via gateways to the public network to reach locations not on the private network. Tymnet was also connected to dozens of other public networks in the U.S. and internationally via X.25/X.75 gateways. (Interesting note: Tymnet was not named after Mr. Tyme. Another employee suggested the name.)"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 79 Chat"
    When I send a message with content "What did Tymnet connect "
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "connect host computers (servers)at thousands of large companies, educational institutions, and government agencies"

  Scenario: SQuAD Sample 80 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 80" and content "Ctenophora (/tᵻˈnɒfərə/; singular ctenophore, /ˈtɛnəfɔːr/ or /ˈtiːnəfɔːr/; from the Greek κτείς kteis 'comb' and φέρω pherō 'carry'; commonly known as comb jellies) is a phylum of animals that live in marine waters worldwide. Their most distinctive feature is the ‘combs’ – groups of cilia which they use for swimming – they are the largest animals that swim by means of cilia. Adults of various species range from a few millimeters to 1.5 m (4 ft 11 in) in size. Like cnidarians, their bodies consist of a mass of jelly, with one layer of cells on the outside and another lining the internal cavity. In ctenophores, these layers are two cells deep, while those in cnidarians are only one cell deep. Some authors combined ctenophores and cnidarians in one phylum, Coelenterata, as both groups rely on water flow through the body cavity for both digestion and respiration. Increasing awareness of the differences persuaded more recent authors to classify them as separate phyla."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 80 Chat"
    When I send a message with content "What does ctenophora rely on for digestion and respiration?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "water flow through the body cavity"

  Scenario: SQuAD Sample 81 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 81" and content "Free oxygen gas was almost nonexistent in Earth's atmosphere before photosynthetic archaea and bacteria evolved, probably about 3.5 billion years ago. Free oxygen first appeared in significant quantities during the Paleoproterozoic eon (between 3.0 and 2.3 billion years ago). For the first billion years, any free oxygen produced by these organisms combined with dissolved iron in the oceans to form banded iron formations. When such oxygen sinks became saturated, free oxygen began to outgas from the oceans 3–2.7 billion years ago, reaching 10% of its present level around 1.7 billion years ago."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 81 Chat"
    When I send a message with content "At first, what did oxygen and iron combine to form?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "banded iron formations"

  Scenario: SQuAD Sample 82 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 82" and content "Evolution of the adaptive immune system occurred in an ancestor of the jawed vertebrates. Many of the classical molecules of the adaptive immune system (e.g., immunoglobulins and T cell receptors) exist only in jawed vertebrates. However, a distinct lymphocyte-derived molecule has been discovered in primitive jawless vertebrates, such as the lamprey and hagfish. These animals possess a large array of molecules called Variable lymphocyte receptors (VLRs) that, like the antigen receptors of jawed vertebrates, are produced from only a small number (one or two) of genes. These molecules are believed to bind pathogenic antigens in a similar way to antibodies, and with the same degree of specificity."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 82 Chat"
    When I send a message with content "What molecules of the adaptive immune system only exist in jawed vertebrates?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "immunoglobulins and T cell receptors"

  Scenario: SQuAD Sample 83 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 83" and content "After al-Nimeiry was overthrown in 1985 the party did poorly in national elections, but in 1989 it was able to overthrow the elected post-al-Nimeiry government with the help of the military. Turabi was noted for proclaiming his support for the democratic process and a liberal government before coming to power, but strict application of sharia law, torture and mass imprisonment of the opposition, and an intensification of the long-running war in southern Sudan, once in power. The NIF regime also harbored Osama bin Laden for a time (before 9/11), and worked to unify Islamist opposition to the American attack on Iraq in the 1991 Gulf War."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 83 Chat"
    When I send a message with content "When was al-Nimeiry accepted?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 84 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 84" and content "In September 1760, and before any hostilities erupted, Governor Vaudreuil negotiated from Montreal a capitulation with General Amherst. Amherst granted Vaudreuil's request that any French residents who chose to remain in the colony would be given freedom to continue worshiping in their Roman Catholic tradition, continued ownership of their property, and the right to remain undisturbed in their homes. The British provided medical treatment for the sick and wounded French soldiers and French regular troops were returned to France aboard British ships with an agreement that they were not to serve again in the present war."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 84 Chat"
    When I send a message with content "What French General negotiated at Montreal?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 85 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 85" and content "All Recognized Student Organizations, from the University of Chicago Scavenger Hunt to Model UN, in addition to academic teams, sports club, arts groups, and more are funded by The University of Chicago Student Government. Student Government is made up of graduate and undergraduate students elected to represent members from their respective academic unit. It is led by an Executive Committee, chaired by a President with the assistance of two Vice Presidents, one for Administration and the other for Student Life, elected together as a slate by the student body each spring. Its annual budget is greater than $2 million."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 85 Chat"
    When I send a message with content "The student government is led by the president and chaired by who?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 86 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 86" and content "The Daily Mail newspaper reported in 2012 that the UK government's benefits agency was checking claimants' \"Sky TV bills to establish if a woman in receipt of benefits as a single mother is wrongly claiming to be living alone\" – as, it claimed, subscription to sports channels would betray a man's presence in the household. In December, the UK’s parliament heard a claim that a subscription to BSkyB was ‘often damaging’, along with alcohol, tobacco and gambling. Conservative MP Alec Shelbrooke was proposing the payments of benefits and tax credits on a \"Welfare Cash Card\", in the style of the Supplemental Nutrition Assistance Program, that could be used to buy only \"essentials\"."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 86 Chat"
    When I send a message with content "What did Alec Shelbrooke propose payments of benefits never be made on?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 87 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 87" and content "At the start of the war, no French regular army troops were stationed in North America, and few British troops. New France was defended by about 3,000 troupes de la marine, companies of colonial regulars (some of whom had significant woodland combat experience). The colonial government recruited militia support when needed. Most British colonies mustered local militia companies, generally ill trained and available only for short periods, to deal with native threats, but did not have any standing forces."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 87 Chat"
    When I send a message with content "What was abnormal British defense?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 88 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 88" and content "Fresno is marked by a semi-arid climate (Köppen BSh), with mild, moist winters and hot and dry summers, thus displaying Mediterranean characteristics. December and January are the coldest months, and average around 46.5 °F (8.1 °C), and there are 14 nights with freezing lows annually, with the coldest night of the year typically bottoming out below 30 °F (−1.1 °C). July is the warmest month, averaging 83.0 °F (28.3 °C); normally, there are 32 days of 100 °F (37.8 °C)+ highs and 106 days of 90 °F (32.2 °C)+ highs, and in July and August, there are only three or four days where the high does not reach 90 °F (32.2 °C). Summers provide considerable sunshine, with July peaking at 97 percent of the total possible sunlight hours; conversely, January is the lowest with only 46 percent of the daylight time in sunlight because of thick tule fog. However, the year averages 81% of possible sunshine, for a total of 3550 hours. Average annual precipitation is around 11.5 inches (292.1 mm), which, by definition, would classify the area as a semidesert. Most of the wind rose direction occurrences derive from the northwest, as winds are driven downward along the axis of the California Central Valley; in December, January and February there is an increased presence of southeastern wind directions in the wind rose statistics. Fresno meteorology was selected in a national U.S. Environmental Protection Agency study for analysis of equilibrium temperature for use of ten-year meteorological data to represent a warm, dry western United States locale."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 88 Chat"
    When I send a message with content "How many days does the high not reach 90 in December?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 89 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 89" and content "DECnet is a suite of network protocols created by Digital Equipment Corporation, originally released in 1975 in order to connect two PDP-11 minicomputers. It evolved into one of the first peer-to-peer network architectures, thus transforming DEC into a networking powerhouse in the 1980s. Initially built with three layers, it later (1982) evolved into a seven-layer OSI-compliant networking protocol. The DECnet protocols were designed entirely by Digital Equipment Corporation. However, DECnet Phase II (and later) were open standards with published specifications, and several implementations were developed outside DEC, including one for Linux."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 89 Chat"
    When I send a message with content "What did DECnet Phase I become?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 90 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 90" and content "The Computer Science Network (CSNET) was a computer network funded by the U.S. National Science Foundation (NSF) that began operation in 1981. Its purpose was to extend networking benefits, for computer science departments at academic and research institutions that could not be directly connected to ARPANET, due to funding or authorization limitations. It played a significant role in spreading awareness of, and access to, national networking and was a major milestone on the path to development of the global Internet."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 90 Chat"
    When I send a message with content "What was considered to be a major milestone?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 91 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 91" and content "Wealth concentration is a theoretical[according to whom?] process by which, under certain conditions, newly created wealth concentrates in the possession of already-wealthy individuals or entities. According to this theory, those who already hold wealth have the means to invest in new sources of creating wealth or to otherwise leverage the accumulation of wealth, thus are the beneficiaries of the new wealth. Over time, wealth condensation can significantly contribute to the persistence of inequality within society. Thomas Piketty in his book Capital in the Twenty-First Century argues that the fundamental force for divergence is the usually greater return of capital (r) than economic growth (g), and that larger fortunes generate higher returns [pp. 384 Table 12.2, U.S. university endowment size vs. real annual rate of return]"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 91 Chat"
    When I send a message with content "According to the wealth concentration theory, what advantage do the wealthy have in accumulating new wealth?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "means to invest"

  Scenario: SQuAD Sample 92 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 92" and content "The origin of the legendary figure is not fully known. The best-known legend, by Artur Oppman, is that long ago two of Triton's daughters set out on a journey through the depths of the oceans and seas. One of them decided to stay on the coast of Denmark and can be seen sitting at the entrance to the port of Copenhagen. The second mermaid reached the mouth of the Vistula River and plunged into its waters. She stopped to rest on a sandy beach by the village of Warszowa, where fishermen came to admire her beauty and listen to her beautiful voice. A greedy merchant also heard her songs; he followed the fishermen and captured the mermaid."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 92 Chat"
    When I send a message with content "What did a greedy merchant do to the mermaid?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "captured"

  Scenario: SQuAD Sample 93 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 93" and content "Following the treaty, King George III issued the Royal Proclamation of 1763 on October 7, 1763, which outlined the division and administration of the newly conquered territory, and to some extent continues to govern relations between the government of modern Canada and the First Nations. Included in its provisions was the reservation of lands west of the Appalachian Mountains to its Indian population, a demarcation that was at best a temporary impediment to a rising tide of westward-bound settlers. The proclamation also contained provisions that prevented civic participation by the Roman Catholic Canadians. When accommodations were made in the Quebec Act in 1774 to address this and other issues, religious concerns were raised in the largely Protestant Thirteen Colonies over the advance of \"popery\"; the Act maintained French Civil law, including the seigneurial system, a medieval code soon to be removed from France within a generation by the French Revolution."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 93 Chat"
    When I send a message with content "What was the objective of Royal Proclamation of 1763?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "outlined the division and administration of the newly conquered territory"

  Scenario: SQuAD Sample 94 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 94" and content "Since the IPCC does not carry out its own research, it operates on the basis of scientific papers and independently documented results from other scientific bodies, and its schedule for producing reports requires a deadline for submissions prior to the report's final release. In principle, this means that any significant new evidence or events that change our understanding of climate science between this deadline and publication of an IPCC report cannot be included. In an area of science where our scientific understanding is rapidly changing, this has been raised as a serious shortcoming in a body which is widely regarded as the ultimate authority on the science. However, there has generally been a steady evolution of key findings and levels of scientific confidence from one assessment report to the next.[citation needed]"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 94 Chat"
    When I send a message with content "What organization is responsible for their own research?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 95 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 95" and content "Non-revolutionary civil disobedience is a simple disobedience of laws on the grounds that they are judged \"wrong\" by an individual conscience, or as part of an effort to render certain laws ineffective, to cause their repeal, or to exert pressure to get one's political wishes on some other issue. Revolutionary civil disobedience is more of an active attempt to overthrow a government (or to change cultural traditions, social customs, religious beliefs, etc...revolution doesn't have to be political, i.e. \"cultural revolution\", it simply implies sweeping and widespread change to a section of the social fabric). Gandhi's acts have been described as revolutionary civil disobedience. It has been claimed that the Hungarians under Ferenc Deák directed revolutionary civil disobedience against the Austrian government. Thoreau also wrote of civil disobedience accomplishing \"peaceable revolution.\" Howard Zinn, Harvey Wheeler, and others have identified the right espoused in The Declaration of Independence to \"alter or abolish\" an unjust government to be a principle of civil disobedience."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 95 Chat"
    When I send a message with content "What group of people performed revolutionary civil disobedience toward the Austrian government?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Hungarians"

  Scenario: SQuAD Sample 96 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 96" and content "Lobates have eight comb-rows, originating at the aboral pole and usually not extending beyond the body to the lobes; in species with (four) auricles, the cilia edging the auricles are extensions of cilia in four of the comb rows. Most lobates are quite passive when moving through the water, using the cilia on their comb rows for propulsion, although Leucothea has long and active auricles whose movements also contribute to propulsion. Members of the lobate genera Bathocyroe and Ocyropsis can escape from danger by clapping their lobes, so that the jet of expelled water drives them backwards very quickly. Unlike cydippids, the movements of lobates' combs are coordinated by nerves rather than by water disturbances created by the cilia, yet combs on the same row beat in the same Mexican wave style as the mechanically coordinated comb rows of cydippids and beroids. This may have enabled lobates to grow larger than cydippids and to have shapes that are less egg-like."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 96 Chat"
    When I send a message with content "What happens when bathocyroe and ocyropsis clap their lobes together?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "jet of expelled water drives them backwards very quickly."

  Scenario: SQuAD Sample 97 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 97" and content "The Maroons compete in the NCAA's Division III as members of the University Athletic Association (UAA). The university was a founding member of the Big Ten Conference and participated in the NCAA Division I Men's Basketball and Football and was a regular participant in the Men's Basketball tournament. In 1935, the University of Chicago reached the Sweet Sixteen. In 1935, Chicago Maroons football player Jay Berwanger became the first winner of the Heisman Trophy. However, the university chose to withdraw from the conference in 1946 after University President Robert Maynard Hutchins de-emphasized varsity athletics in 1939 and dropped football. (In 1969, Chicago reinstated football as a Division III team, resuming playing its home games at the new Stagg Field.)"
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 97 Chat"
    When I send a message with content "The Maroons compete in what league division?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "NCAA's Division III"

  Scenario: SQuAD Sample 98 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 98" and content "French Huguenots made two attempts to establish a haven in North America. In 1562, naval officer Jean Ribault led an expedition that explored Florida and the present-day Southeastern U.S., and founded the outpost of Charlesfort on Parris Island, South Carolina. The Wars of Religion precluded a return voyage, and the outpost was abandoned. In 1564, Ribault's former lieutenant René Goulaine de Laudonnière launched a second voyage to build a colony; he established Fort Caroline in what is now Jacksonville, Florida. War at home again precluded a resupply mission, and the colony struggled. In 1565 the Spanish decided to enforce their claim to La Florida, and sent Pedro Menéndez de Avilés, who established the settlement of St. Augustine near Fort Caroline. Menéndez' forces routed the French and executed most of the Protestant captives."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 98 Chat"
    When I send a message with content "Which Spanish officer established the settlement at St. Augustine?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Pedro Menéndez de Avilés"

  Scenario: SQuAD Sample 99 - Unanswerable
    Given I have uploaded a document with name "SQuAD Sample 99" and content "The internal cavity forms: a mouth that can usually be closed by muscles; a pharynx (\"throat\"); a wider area in the center that acts as a stomach; and a system of internal canals. These branch through the mesoglea to the most active parts of the animal: the mouth and pharynx; the roots of the tentacles, if present; all along the underside of each comb row; and four branches round the sensory complex at the far end from the mouth – two of these four branches terminate in anal pores. The inner surface of the cavity is lined with an epithelium, the gastrodermis. The mouth and pharynx have both cilia and well-developed muscles. In other parts of the canal system, the gastrodermis is different on the sides nearest to and furthest from the organ that it supplies. The nearer side is composed of tall nutritive cells that store nutrients in vacuoles (internal compartments), germ cells that produce eggs or sperm, and photocytes that produce bioluminescence. The side furthest from the organ is covered with ciliated cells that circulate water through the canals, punctuated by ciliary rosettes, pores that are surrounded by double whorls of cilia and connect to the mesoglea."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 99 Chat"
    When I send a message with content "What is the mesoglea situated along the underside of?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: SQuAD Sample 100 - Answerable
    Given I have uploaded a document with name "SQuAD Sample 100" and content "French Huguenots made two attempts to establish a haven in North America. In 1562, naval officer Jean Ribault led an expedition that explored Florida and the present-day Southeastern U.S., and founded the outpost of Charlesfort on Parris Island, South Carolina. The Wars of Religion precluded a return voyage, and the outpost was abandoned. In 1564, Ribault's former lieutenant René Goulaine de Laudonnière launched a second voyage to build a colony; he established Fort Caroline in what is now Jacksonville, Florida. War at home again precluded a resupply mission, and the colony struggled. In 1565 the Spanish decided to enforce their claim to La Florida, and sent Pedro Menéndez de Avilés, who established the settlement of St. Augustine near Fort Caroline. Menéndez' forces routed the French and executed most of the Protestant captives."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "SQuAD Sample 100 Chat"
    When I send a message with content "What was the name of the first Huguenot outpost in South Carolina?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
    And the message content should be relevant to the answer "Charlesfort"

