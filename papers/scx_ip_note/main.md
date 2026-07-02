# SCX
66|项目成果归属说明

**Author:** SCX

64|
65|## SCX
66|项目成果归属说明<!-- label: scx-ux9879ux76eeux6210ux679cux5f52ux5c5eux8bf4ux660e -->
67|
68|
> 69|本文件记录 SCX (State-Conditioned eXpertise)
> 70|项目的知识产权归属与独立性声明。 最后更新：2026-06-26
> 71|

72|
73|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

74|
75|### 一、SCX
76|项目独立性声明<!-- label: ux4e00scx-ux9879ux76eeux72ecux7acbux6027ux58f0ux660e -->
77|
78|#### 1.1 核心性质：SCX 是纯数学/ML
79|框架<!-- label: ux6838ux5fc3ux6027ux8d28scx-ux662fux7eafux6570ux5b66ml-ux6846ux67b6 -->
80|
81|SCX 是**状态条件专家性**（State-Conditioned
82|eXpertise）的数学框架，其核心贡献是：
83|
84|
- 
- 
- 

94|
95|SCX **不包含**任何 DFT（密度泛函理论）计算代码、VASP
96|输入文件、或材料科学特定的计算逻辑。
97|
98|#### 1.2
99|不依赖学校资源<!-- label: ux4e0dux4f9dux8d56ux5b66ux6821ux8d44ux6e90 -->
100|
101|\begin{longtable}[]{@{}
102|  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2247}}
103|  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1348}}
104|  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.6404}}@{}}
105|\toprule\noalign{}
106|\begin{minipage}[b]
107|资源
108|\end{minipage} & \begin{minipage}[b]
109|是否使用
110|\end{minipage} & \begin{minipage}[b]
111|说明
112|\end{minipage} 

113|\midrule\noalign{}
114|\endhead
115|\bottomrule\noalign{}
116|\endlastfoot
117|孝感超算（学校设备） & **否** & SCX
118|所有理论工作、编码、实验均在个人电脑完成 

119|学校网络/存储 & **否** & SCX 项目存储于个人电脑和用户个人 GitHub
120|账户 

121|学校软件许可 & **否** & SCX 仅使用开源 Python 包（numpy, scipy,
122|scikit-learn 等） 

123|学校人员/学生 & **否** & SCX 为单人（用户）独立完成 

124|\end{longtable}
125|
126|#### 1.3 实验独立性<!-- label: ux5b9eux9a8cux72ecux7acbux6027 -->
127|
128|SCX 的验证实验包括三类：
129|
130|
1. 
2. 
3. 

143|
144|
> 145|合成数据 + 公开基准数据集已足以验证 SCX 的所有核心主张。MLIP
> 146|案例纯粹是''锦上添花''的附加展示。
> 147|

148|
149|#### 1.4 AI
150|代码生成声明<!-- label: ai-ux4ee3ux7801ux751fux6210ux58f0ux660e -->
151|
152|SCX Python 包的**全部代码**由 AI 工具 **AI programming tools
153|(AI)** 在用户的数学框架和设计方向指导下生成。用户是：
154|
155|
- 
- 
- 

164|
165|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

166|
167|### 二、与 EGP / AlGaN / DFT
168|项目的边界<!-- label: ux4e8cux4e0e-egp-algan-dft-ux9879ux76eeux7684ux8fb9ux754c -->
169|
170|#### 2.1
171|两个独立项目<!-- label: ux4e24ux4e2aux72ecux7acbux9879ux76ee -->
172|
173|\begin{longtable}[]{@{}lll@{}}
174|\toprule\noalign{}
175|维度 & EGP 项目（Paper 1-3） & SCX 项目（Paper 4） 

176|\midrule\noalign{}
177|\endhead
178|\bottomrule\noalign{}
179|\endlastfoot
180|本质 & MLIP（机器学习势函数） & 通用的 ML 理论框架 

181|依赖 & 依赖 DFT 数据（AlN v3） & 不依赖任何 DFT 数据 

182|计算资源 & 使用孝感超算 & 个人电脑即可 

183|应用领域 & 材料科学 & 通用机器学习 

184|代码仓库 & `egp/` & `SCX/` 

185|\end{longtable}
186|
187|#### 2.2
188|唯一交集：概念起源<!-- label: ux552fux4e00ux4ea4ux96c6ux6982ux5ff5ux8d77ux6e90 -->
189|
190|SCX 中**``状态条件专家性''**这一核心概念的思想萌芽来自 EGP Paper 1
191|的 gauge fixing 工作------在拼接多个 ACE/PACE
192|势函数时，用户观察到同一势函数在不同构型区域上的精度不同。
193|
194|然而，**SCX
195|框架本身完全不涉及势函数、DFT、或任何材料科学内容**。它是一个通用 ML
196|理论框架，将''状态条件专家性''形式化为可用于任何监督学习场景的数学框架（数据价值评估、主动学习、专家路由、数据压缩）。
197|
198|
> 199|**类比**：牛顿在观察苹果落地时萌生了万有引力的想法，但万有引力定律是一个普适物理理论，不依赖于苹果的具体种类。
> 200|

201|
202|#### 2.3 EGP 项目的 DFT
203|数据权属<!-- label: egp-ux9879ux76eeux7684-dft-ux6570ux636eux6743ux5c5e -->
204|
205|AlN v3 DFT 数据是在**孝感超算**（学校设备）上使用 VASP 生成的，属于
206|EGP 项目的成果。SCX 项目**不声称对这部分数据拥有独立所有权**。SCX
207|框架的可验证性不依赖这些数据。
208|
209|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

210|
211|### 三、与学校/课题组的关系说明<!-- label: ux4e09ux4e0eux5b66ux6821ux8bfeux9898ux7ec4ux7684ux5173ux7cfbux8bf4ux660e -->
212|
213|#### 3.1 切割声明<!-- label: ux5207ux5272ux58f0ux660e -->
214|
215|
- 
- 
- 
- 
- 

228|
229|#### 3.2
230|潜在关联与排除<!-- label: ux6f5cux5728ux5173ux8054ux4e0eux6392ux9664 -->
231|
232|SCX
233|项目与用户所在课题组之间**没有雇佣、资助或指导关系**。即使存在任何课题组的通用知识（如
234|ML 基础），SCX
235|的理论创新------状态条件专家性的数学框架------是用户在个人时间独立提出的原创贡献。
236|
237|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

238|
239|### 四、权属声明模板<!-- label: ux56dbux6743ux5c5eux58f0ux660eux6a21ux677f -->
240|
241|#### 4.1 所有权归属<!-- label: ux6240ux6709ux6743ux5f52ux5c5e -->
242|
243|SCX 项目的所有权利（包括但不限于版权、专利权、署名权）归属：
244|
245|
> 246|**【预留：填写权利人信息】**
> 247|
> 248|姓名：SCX
> 249|日期：\_\_\_\_\_\_\_\_\_\_\_\_\_2026.06.26\_\_\_\_\_\_\_\_\_\_\_\_\_
> 250|

251|
252|#### 4.2 代码许可<!-- label: ux4ee3ux7801ux8bb8ux53ef -->
253|
254|SCX Python 包的发布许可待定。目前为私密仓库，不对外分发。
255|
256|#### 4.3 论文署名<!-- label: ux8bbaux6587ux7f72ux540d -->
257|
258|如发表学术论文，SCX 的署名权根据独立贡献程度决定：
259|
260|\begin{longtable}[]{@{}ll@{}}
261|\toprule\noalign{}
262|贡献 & 角色 

263|\midrule\noalign{}
264|\endhead
265|\bottomrule\noalign{}
266|\endlastfoot
267|数学框架（定义、命题、证明） & **用户**（100\%） 

268|架构设计 & **用户**（100\%） 

269|代码实现 & AI (AI programming tools) 按用户指导生成 

270|实验设计和执行 & **用户**（100\%） 

271|\end{longtable}
272|
273|
> 274|**AI 工具不享有署名权**。根据学术出版规范（COPE, Nature, arXiv
> 275|等），AI 工具不得列为作者，但应在致谢或方法部分声明其使用。
> 276|

277|
278|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

279|
280|### 五、法律与伦理声明<!-- label: ux4e94ux6cd5ux5f8bux4e0eux4f26ux7406ux58f0ux660e -->
281|
282|本文件所陈述的内容如实反映 SCX
283|项目的开发过程、资源使用情况和贡献归属。如有争议，保留通过以下方式进一步证明的权利：
284|
285|
1. 
2. 
3. 
4. 

297|
298|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

299|
300|*本文件由用户于 2026-06-26 撰写，用于记录 SCX 项目的知识产权状况。*
301|
302|
303|