# 🎯 Challenges to Be Solved
## التحديات التي تحتاج حل

---

## 📋 قائمة التحديات:

<!-- أضف التحديات هنا -->



---
1. ملخص تنفيذي للثغرات الجوهرية

المنتج مصمَّم فعليًا لعقل مهندس، بينما الجمهور المستهدف في ملف الألم هو مستخدم غير تقني لا يقرأ الكود ولا يفهم البنية.

الاعتماد المعماري الأساسي على Static Context Injection عبر ملف Markdown واحد ضخم (guardian.mdc) أصبح نقطة ضعف:

تضخيم السياق.

تشتيت النموذج.

صعوبة التوسّع مع المشاريع المتوسطة والكبيرة.

فهم الكود مبني تقريبًا بالكامل على Regex + Heuristics سطحية بدون أي AST أو فهم لغوي حقيقي، ما يجعل “الذكاء” في الماسح وهميًا في المشاريع المعقّدة.

لا توجد طبقة enforcement تقنية حقيقية:

LOCKED / DANGER / RULES مجرد نصوص، ليس هناك Gate واضح يمنع الوكيل من كسرها.

المزامنة بين الكود والذاكرة عرضة للتخلّف والتضارب:

Watcher يعيد مسح المشروع كاملًا مع كل تغيير.

pre-commit hook يتخطى التحديث بسهولة.

المشروع لا يغطّي فعليًا أغلب نقاط الألم الـ 26 في ملفك، بل يلامس بعضها بشكل توثيقي لا تنفيذي.

مقارنة بالأدوات المتقدمة (Aider, Cursor, CLAUDE.md, Copilot Instructions)، Guardian-H ما زال في مستوى “حل brute-force قبل عصر الـ embeddings و الـ RAG”.

2. ثغرات على مستوى الفكرة والمعمارية
2.1 فجوة الجمهور المستهدف

ملف الألم يصف مستخدمًا:

لا يقرأ الكود.

لا يفهم البنية.

لا يستطيع التحقق من صحة اقتراحات الوكيل.

يثق بالوكيل ثقة شبه كاملة.

Guardian-H الحالي يتطلّب:

تشغيل أوامر CLI (curl | bash, pip install, pre-commit).

فهم فكرة guardian.mdc وقراءته.

التعامل مع أخطاء المسح، hooks، watcher.

النتيجة: المنتج حاليًا يخدم “المهندس الذي يبني حارسًا للمستخدم”، وليس المستخدم نفسه الذي يعاني من المشاكل المذكورة في Pain Points.

2.2 وهم "الذكاء" عبر Regex (Regex Illusion)

guardian_scanner.py و scanner.js يعتمدان على:

Regex لاستخراج الدوال.

استنتاج “purpose” الملف من اسم المجلد واسم الملف فقط.

لا يوجد:

AST.

تحليل imports / call graph.

فهم domain modules.

الأثر:
الماسح “يخمن” أكثر مما “يفهم”؛ في نماذج كود غير تقليدية أو مشاريع كبيرة، كثير من التصنيفات (FILES, functions, purpose) ستكون مضللة.

2.3 تضخّم السياق (Context Window Pollution)

guardian.mdc يحتوي على:

TECH_STACK، FILES، DEPENDENCIES، ENV_VARS، CONNECTIONS، RUN.

AGENT_RULES, LOCKED, DANGER, CHANGES.

أنماط تفكير ومبادئ من THINKING_PATTERNS, CODE_PRINCIPLES.

هذا الملف يُفترض حقنه في سياق الوكيل بشكل دائم.

المشكلة:

في المشاريع المتوسطة/الكبيرة:

الملف سيتضخم بسرعة.

استهلاك tokens مرتفع وثابت.

النموذج يتلقى معلومات كثيرة لا علاقة لها بالمهمة الحالية → Attention Dilution وتقليل الدقّة.

2.4 فخ التزامن (Synchronization Latency)

guardian_watcher.py:

يعتمد على watchdog.

يعيد تشغيل المسح الكامل بعد DEBOUNCE_TIME=2 ثانية عند أي تغيير.

الثغرات:

فجوة زمنية: الوكيل قد يتعامل مع guardian.mdc قديم (قبل تحديثه).

التكلفة: إعادة مسح المشروع كاملًا لكل تعديل بسيط → I/O مبالغ فيها ومشاكل أداء مع مشاريع Node.js/monorepos.

2.5 الاعتماد الساذج على التزام الوكيل (Prompt Compliance)

كل الحماية مبنية على جملة “اقرأ AGENT_RULES والتزم بها”.

LLMs:

غير حتمية.

تعاني من Lost-in-the-Middle.

قد تتجاهل التعليمات البعيدة في السياق عند محادثات طويلة.

النتيجة:
لا يوجد Hard Constraint يمنع الوكيل من:

إنشاء ملفات مكرّرة.

تعديل ملفات Locked.

حذف ملفات مهمة.

كل شيء توصية نصّية، لا حارس فعلي.

3. ثغرات في تصميم ملف guardian.mdc
3.1 ملف واحد متضخّم ومتعدد الأدوار

يجمع:

قواعد الوكيل.

Snapshot تقني.

قرارات Locked.

Change log.

أنماط تفكير ومبادئ عامة.

العيوب:

يخالف أفضل الممارسات في:

CLAUDE.md.

.cursor/rules/*.mdc.

.github/copilot-instructions.

يصعّب تمييز:

ما هو “دستور قاسٍ”.

ما هو “معلومة سياقية”.

ما هو “إرشاد فكري” (patterns).

3.2 ثنائية اللغة داخل ملف واحد

خلط عربي + إنجليزي في نفس الأقسام والقواعد.

تضاعف حجم الملف بدون إضافة معرفة جديدة للـ LLM.

يزيد استهلاك التوكنز ويضيف ضجيجًا لغويًا.

3.3 TECH_STACK و DEPENDENCIES سطحية وغير شاملة

TECH_STACK:

مبني على package.json و requirements.txt فقط.

لا يدعم: Ruby, Laravel, Go, Rust, .NET … رغم أن الامتدادات موجودة في CODE_EXTENSIONS.

DEPENDENCIES:

Python: كل شيء غير name==version يُعتبر “latest” افتراضيًا، وهذا افتراض غير دقيق.

JS: التحيز لقائمة محدودة من الـ libs “المهمة”، ما يخلق لا اتساق بين JS و Python.

3.4 ENV_VARS بلا قيمة عملية

قراءة .env.example / .env.sample وتحويلها إلى قائمة متغيرات بـ:

description = "TODO".

لا تمييز بين:

required vs optional.

secret vs config عادي.

لا نوع بيانات، لا مدى مقبول.

3.5 FILES و CONNECTIONS نايفية

FILES:

قائمة مسطحة دون grouping حسب domain أو service.

“purpose” مبني على اسم المجلد فقط.

functions[:10] فقط من كل ملف → قد يتجاهل أهم الدوال في الأسفل.

CONNECTIONS:

أي رقم يشبه port يُلتقط كـ اتصال.

لا تمييز بين port فعلي وأرقام أخرى.

لا ربط بين port واسم الخدمة أو env variable.

3.6 RUN محدود جدًا

يعتمد على أنماط بسيطة:

npm run dev / npm start.

uvicorn main:app --reload.

لا يدعم:

monorepos.

Yarn/pnpm/Poetry/Pipenv.

سيناريوهات متعددة للتشغيل (backend, dashboard, worker…).

4. ثغرات في الماسحات (Python / JS)
4.1 تغطية لغات بلا دعم فعلي

CODE_EXTENSIONS تشمل معظم لغات العالم.

tech_stack والتحليل الحقيقي فقط لـ:

Python (FastAPI/Django/Flask).

JS/TS (React/Vue/Next/Express…).

النتيجة:
في مشاريع Java / Go / Rust / .NET:

Guardian يظهر وكأنه “يدعمها”، لكنه عمليًا لا ينتج Tech Stack أو فهمًا فعليًا.

4.2 تجاهل .gitignore وأنماط الـ Data/Logs

يتم تجاهل SKIP_DIRS hard-coded (node_modules, dist, .next…).

أي مجلد آخر ثقيل (logs, dumps, tmp) قد يُمسح بلا داعٍ، مما يزيد الزمن والتكلفة.

4.3 تحليل دوال JS/TS بالـ Regex فقط

لا يفهم:

class methods.

object methods.

inline arrow functions المعقدة.

يضيف functions محدودة في FILES، ما يعطي صورة ناقصة للوكيل.

4.4 قراءة ملفات Binary أو غريبة

BINARY_EXTENSIONS قائمة ثابتة.

أي نوع غير معروف قد يُقرأ كنص، مما ينتج garbage text أو crashes محتملة.

4.5 الأداء: تمريرات متعددة على نفس الشجرة

استخدام rglob متكرر لكل نوع امتداد بدلاً من تمريرة واحدة وتصنيف حسب الامتداد.

غير مناسب مع مشاريع كبيرة أو monorepos.

5. ثغرات في GuardianMemory و MCP Server
5.1 GuardianMemory: Parsing هشّ

parsing لـ guardian.mdc بالكامل بالـ regex:

get_section يعتمد على عناوين ##.

add_file/add_change تحقن نصًا بعد header بعينه.

أي تغيير بسيط في تنسيق Markdown يكسر المنطق.

5.2 ChangeClassifier: تصنيف بدائي جدًا

يعتمد على presence لكلمات مثل: color, style, button, page, feature…

لا يأخذ سياق الجملة:

"The color of the button logic is wrong" → يصنفها UI_STYLE رغم أن المشكلة logic.

التصنيف لا يستخدم:

خريطة الملفات.

نوع الملفات المتأثرة.

حجم diff.

5.3 غياب Vector Store / Semantic Memory

لا يوجد Embeddings ولا بحث دلالي.

الذاكرة:

Flat Text.

عمليات بحث نصي مباشر.

لا يمكن ربط مفاهيم متقاربة لا تشترك في نفس الكلمات.

5.4 عدم استخدام LOCKED / FILES كـ Gate حقيقي

MCP tools تعيد معلومات مفيدة، لكن:

لا تمنع عمليات خطرة.

لا تفرض سلوكًا معيّنًا على أدوات مثل Cursor أو Antigravity.

التزام الوكيل اختياري بالكامل.

6. ثغرات في التوزيع، CLI، hooks، watcher

install.sh غير آمن:

نمط curl | bash على GitHub main.

أي اختراق للـ repo يتحول لكود يُنفذ مباشرة على أجهزة المستخدمين.

pre-commit hook ضعيف:

إذا لم يجد scanner → يطبع “skipping snapshot update” ويكمل commit.

لا يوجد خيار “لا commit بدون تحديث guardian.mdc”.

watcher مستقل عن باقي النظام:

لا دمج حقيقي معه في README كمسار رسمي.

لا ربط بين watcher و MCP أو IDE integration.

tests ليست اختبارات قياسية:

سكربتات طباعة بدائية، لا pytest / CI واضحة.

لا تغطية لسيناريوهات edge التي ذكرتها في Pain Points.

7. الفجوة مع ملف Pain Points

باختصار:

محاور الألم:

الذاكرة والسياق.

الملفات والبنية.

التحقق والصدق.

القرارات التقنية.

التوثيق.

طول المحادثة.

آثار التعديلات الجانبية.

Guardian-H الحالي:

يعالج جزءًا من (1) و (5) بشكل توثيقي فقط عبر snapshot ثابت.

يلامس (2) و (4) محتوىً، لكنه لا يقدّم enforcement الآلي.

لا يعالج فعليًا (3), (6), (7) إلا على مستوى نوايا وأفكار في النصوص.

تقدير تقريبي:

~30–40٪ من المشاكل مغطّاة نظريًا.

الجزء الأكبر من الألم العملي (verification, gating, dynamic context, conflict resolution) ما زال بلا حل تنفيذي.

8. مقارنة مباشرة مع Aider و Cursor
8.1 نوع الذاكرة

Guardian-H:
Static Snapshot عبر ملف Markdown واحد.

Aider:

Dynamic Repo Map تعتمد على Tree-sitter و ranking للملفات الأكثر صلة.

Cursor:

Embeddings + Index + Rules؛ يسترجع أجزاء صغيرة حسب الطلب.

8.2 آلية التحديث

Guardian-H:

Rescan كامل عبر watcher أو pre-commit.

Aider:

تحديث لحظي وذكي حسب الملفات التي تمسّها الأوامر.

Cursor:

Indexing في الخلفية مع تكامل عميق مع الـ IDE.

8.3 دقة السياق واستهلاك التوكنز

Guardian-H:

يرسل snapshot شامل أو large chunk دائمًا.

Aider:

يرسل فقط “أهم 1% من الكود” المتعلق بالمهمة الحالية.

Cursor:

RAG-style: يسترجع فقط الملفات/الأسطر ذات الصلة.

8.4 فهم الكود والتحكم في الوكيل

Guardian-H:

Regex + heuristics سطحية.

التحكم عبر نصوص Rules فقط.

Aider:

AST + تحكم في الـ loop (اختيار ما يُرسل للنموذج).

Cursor:

Symbols, References, Context Graph + واجهة IDE تضبط سلوك الوكيل.

الخلاصة المقارنة:
Guardian-H يحاول يدويًا عبر Markdown القيام بما تقوم به هذه الأدوات داخليًا عبر:

AST.

Embeddings.

Context Graph.

Dynamic retrieval.

9. الحكم الحالي (كما هو الآن)

Guardian-H مفيد كـ:

أداة Snapshot وتوثيق آلي لـ “حالة المشروع” في ملف واحد.

Playground فكري لاختبار مفهوم “حارس المشروع” (Guardian Concept).

لكنه غير كافٍ كـ:

حل حقيقي لمشاكل المستخدم غير التقني مع الوكلاء.

Gatekeeper يمنع التخبيص، التكرار، تضارب القرارات، وفوضى الملفات.

منافس فعلي للأدوات التي تستخدم AST + Embeddings + Dynamic Context.

إذا أردت البناء عليه، فالثغرة الجوهرية التي يجب معالجتها ليست في شكل Markdown أو Regex، بل في الانتقال من:

“ذاكرة ثابتة تُحقن كاملة في كل طلب”

إلى:

“خادم سياق حي (Live Context Server) + Rules + Gate”
يعطي الوكيل ما يحتاجه فقط، في اللحظة المناسبة، بناءً على الطلب الفعلي، مع قيود قابلة للتنفيذ وليس مجرد تعليمات نصية.

هذا التقرير يغطي كل الملاحظات السابقة + الملاحظات الجديدة في كتلة النص الأخيرة التي أرسلتها.
