考试阶段，请按照提供的 question_id 完成答卷文件写入。
每次只答一题，写入后等待下一个问题。当下一个问题发送后，你才能答题。

答卷文件位置：
`Evaluation/Manual Answers.md`

每次用户发送 question_id 和 question 后：
1. 打开答卷文件。
2. 根据 question_id 找到对应题目区块。
3. 只填写该区块的 final_answer。答案不直接跟在冒号之后，写在 final_answer: 的下一行。
4. 不要修改 question_id、question、结束标记或其他题目内容。

**格式示例**：
final_answer:
这里填写最终答案。

规则：
- 禁止作弊。如果你不确定，你可以在考试中使用记忆相关的Tools进行回忆，但是不能查阅资料。另外，你可以查阅考试规则说明相关的文件。
- 考试全程使用英文。当你准备好后，请回复 “I'm Ready.”，然后我们开始考试。

