---
description: Default instructions for the Steve's Semantic Similarity Analysis plugin.
  Use this skill whenever this plugin is invoked.
name: instructions
---

You will be comparing two texts for semantic similarity. Here are the texts:

<text1>
{{TEXT1}}
</text1>

<text2>
{{TEXT2}}
</text2>

Analyze these texts according to the following steps:

1. Identify the Theme:
   - Determine the central theme or topic of each text.
   - Assess the similarity between the themes.

2. Analyze Participating Objects:
   - Identify the key objects or entities mentioned in each text.
   - Evaluate the similarity between the objects involved.

3. Examine Activities:
   - Determine the main actions or events described in each text.
   - Assess the similarity between the activities being carried out.

4. Consider Other Factors:
   - Identify any additional factors or nuances present in the texts that might influence their similarity.
   - Evaluate the impact of these factors on the overall similarity.

5. Overall Similarity Assessment:
   - Based on your analysis of the above factors, provide a comprehensive assessment of the semantic similarity between the two texts.
   - Use a scale of 0 to 4, where 0 indicates no similarity and 4 indicates high similarity.

Provide your analysis and assessment in the following format:

<analysis>
1. Theme:
   [Your analysis of themes]

2. Participating Objects:
   [Your analysis of objects]

3. Activities:
   [Your analysis of activities]

4. Other Factors:
   [Your analysis of other factors]
</analysis>

<assessment>
[Your comprehensive assessment of semantic similarity, including justification]
</assessment>

<score>
[Your numerical score from 0 to 4]
</score>

Ensure that your assessment in the <assessment> tags includes a thorough justification for your score before providing the actual numerical score in the <score> tags.