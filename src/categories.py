"""Tool categories. A category goes live automatically once it has at least one tool.
Order here = order on /tools/. Slugs are permanent URLs: never rename a live one."""

H = 'https://brandella.in/tools/seo-tools/'
S = 'https://brandella.in/tools/schema-generators/'
PP = 'https://brandella.in/tools/ppc-calculators/'
AN = 'https://brandella.in/tools/analytics-tools/'
SMU = 'https://brandella.in/tools/social-media-tools/'
TS = 'https://brandella.in/tools/technical-seo-tools/'
GA = 'https://brandella.in/tools/google-ads-tools/'
AI = 'https://brandella.in/tools/ai-tools/'
DV = 'https://brandella.in/tools/developer-tools/'
EM = 'https://brandella.in/tools/email-marketing-tools/'
CW = 'https://brandella.in/tools/content-writing-tools/'

CATEGORIES = [
    dict(slug='seo-tools', short='SEO', name='SEO Tools', pill='SEO',
         card='SERP preview, keyword density, readability, slugs, meta tags, alt text and internal links.',
         hub_title='Free SEO Tools: SERP Preview, Keyword Density and More',
         hub_desc='12 free browser based SEO tools: SERP preview, keyword density, readability, slug generator, meta tags, alt text, internal links and more.',
         hub_lead='Simple, fast SEO tools that run right in your browser. No signup, no limits, and nothing you type ever leaves your device.',
         hub_intro=f'''<h2>Practical SEO Tools for Everyday Work</h2>
    <p>These free SEO tools cover the small but important jobs that come up on almost every page you publish: checking how a result will look in Google, keeping keyword use natural and readable, writing clean URLs and meta tags, fixing headings, alt text and internal links, and building keyword lists.</p>
    <p>Each tool is built by the team behind Brandella Journal and links to an in depth guide, so you can understand the why as well as the how.</p>

    <h2>Which Tool Should You Use?</h2>
    <ul>
      <li><strong>Writing a new page?</strong> Start with the <a href="{H}seo-slug-generator/">SEO Slug Generator</a>, then the <a href="{H}meta-tag-generator/">Meta Tag Generator</a>.</li>
      <li><strong>Before publishing?</strong> Check your result in the <a href="{H}serp-snippet-preview/">SERP Snippet Preview</a> and your outline in the <a href="{H}heading-structure-checker/">Heading Structure Checker</a>.</li>
      <li><strong>Auditing content?</strong> Paste it into the <a href="{H}keyword-density-checker/">Keyword Density Checker</a> and the <a href="{H}readability-score-checker/">Readability Score Checker</a>.</li>
      <li><strong>Checking a live page?</strong> Run its HTML through the <a href="{H}internal-link-checker/">Internal Link Checker</a> and the <a href="{H}alt-text-checker/">Alt Text Checker</a>.</li>
      <li><strong>Building keyword lists?</strong> Use the <a href="{H}keyword-combiner/">Keyword Combiner</a>, then tidy up with the <a href="{H}duplicate-line-remover/">Duplicate Line Remover</a>.</li>
    </ul>
    <p>New to SEO? Read our beginner guide, <a href="https://brandella.in/what-is-seo/">What Is SEO</a>, or compare paid platforms in <a href="https://brandella.in/best-seo-tools-comparison/">our SEO tools comparison</a>.</p>''',
         faqs=[("Are these SEO tools really free?", "Yes. Every tool on this page is free, needs no signup, and has no usage limits."),
               ("Is my data safe?", "All tools run entirely in your browser. Text, HTML and URLs you enter are never uploaded or stored on our servers."),
               ("Will you add more tools?", "Yes. New free tools are added regularly, including schema generators, technical SEO tools and PPC calculators.")]),

    # ---------- ROADMAP (built one per day, in this order) ----------
    dict(slug='schema-generators', short='SC', name='Schema Generators', pill='Schema',
         card='LocalBusiness, Product, Article, Organization, Breadcrumb, Event and Video JSON LD.',
         hub_title='Free Schema Markup Generators: JSON LD for Google',
         hub_desc='Free schema markup generators for LocalBusiness, Product, Article, Organization, Breadcrumb, Event and Video. Create valid JSON LD in seconds.',
         hub_intro=f'''<h2>Which Schema Generator Do You Need?</h2>
    <ul>
      <li><strong>A shop, clinic, cafe or office?</strong> Use the <a href="{S}local-business-schema-generator/">Local Business Schema Generator</a>.</li>
      <li><strong>Selling products?</strong> Use the <a href="{S}product-schema-generator/">Product Schema Generator</a> for price, stock and ratings.</li>
      <li><strong>Publishing posts or news?</strong> Use the <a href="{S}article-schema-generator/">Article Schema Generator</a>, plus the <a href="{S}breadcrumb-schema-generator/">Breadcrumb Schema Generator</a>.</li>
      <li><strong>Your brand and home page?</strong> Use the <a href="{S}organization-schema-generator/">Organization Schema Generator</a>.</li>
      <li><strong>Running a concert, workshop or conference?</strong> Use the <a href="{S}event-schema-generator/">Event Schema Generator</a>.</li>
      <li><strong>Got a video on the page?</strong> Use the <a href="{S}video-schema-generator/">Video Schema Generator</a> to add key moments too.</li>
    </ul>
    <p>Every generator checks your input against Google's current structured data rules as you type, and outputs clean JSON LD you can paste into any page or CMS.</p>

    <h2>Why Is There No FAQ Schema Generator?</h2>
    <p>Google stopped showing FAQ rich results in May 2026, after limiting them to a few government and health sites in 2023. HowTo rich results were removed in 2023 too. FAQPage is still a valid schema.org type, but it no longer earns a special result in Google, so we focus on the types that still do.</p>
    <p>New to structured data? Start with <a href="https://brandella.in/what-is-schema-markup/">what is schema markup</a> and <a href="https://brandella.in/how-to-add-schema-markup-json-ld/">how to add schema markup with JSON LD</a>.</p>''',
         faqs=[("Are these schema generators free?", "Yes. Every generator is free, needs no signup, and has no usage limits."),
               ("Where do I paste the JSON LD code?", "Paste it anywhere in the HTML of the page it describes, usually in the head. In WordPress you can use a custom HTML block or a header code plugin. Then test the page in Google's Rich Results Test."),
               ("Is my data safe?", "Yes. All generators run entirely in your browser. Nothing you type is uploaded or stored.")],
         hub_lead='Create valid JSON LD schema markup for rich results in seconds. Fill in a form, copy the code, and paste it into your page.'),
    dict(slug='ppc-calculators', short='PPC', name='PPC Calculators', pill='PPC',
         card='ROAS, break even ROAS, CPA, CPC, CPM, CTR and PPC budget calculators.',
         hub_title='Free PPC Calculators: ROAS, CPA, CPC, CTR and Budget',
         hub_desc='Free PPC calculators for ROAS, break even ROAS, CPA, CPC, CPM, CTR and ad budgets. Plan and judge Google Ads and Meta campaigns in seconds.',
         hub_lead='Quick, accurate calculators for planning and judging paid campaigns on Google Ads, Meta, LinkedIn and more.',
         hub_intro=f'''<h2>Which PPC Calculator Do You Need?</h2>
    <ul>
      <li><strong>Is my campaign making money?</strong> Use the <a href="{PP}roas-calculator/">ROAS Calculator</a> and the <a href="{PP}cpa-calculator/">CPA Calculator</a>.</li>
      <li><strong>What ROAS do I need?</strong> Find your floor with the <a href="{PP}break-even-roas-calculator/">Break Even ROAS Calculator</a>.</li>
      <li><strong>How much can I bid?</strong> The <a href="{PP}cpc-calculator/">CPC Calculator</a> turns your target CPA into a max CPC.</li>
      <li><strong>Buying display, video or social?</strong> Use the <a href="{PP}cpm-calculator/">CPM Calculator</a> to compare CPM and CPC prices.</li>
      <li><strong>Testing ads?</strong> The <a href="{PP}ctr-calculator/">CTR Calculator</a> tells you if a winner is real.</li>
      <li><strong>Planning next month?</strong> Turn a goal into a daily budget with the <a href="{PP}ppc-budget-calculator/">PPC Budget Calculator</a>.</li>
    </ul>
    <p>Every calculator uses the same formulas Google Ads uses in its own reports, supports rupees and other currencies, and shows a plain English verdict, not just a number.</p>
    <p>New to paid search? Read <a href="https://brandella.in/how-google-ads-auction-works/">how the Google Ads auction works</a> and our <a href="https://brandella.in/25-google-ads-optimization-tips/">Google Ads optimization tips</a>.</p>''',
         faqs=[("Are these PPC calculators free?", "Yes. Every calculator is free, needs no signup, and has no usage limits."),
               ("Do they work for Meta, LinkedIn and Microsoft Ads?", "Yes. ROAS, CPA, CPC, CPM and CTR are calculated the same way on every ad platform. Only the budget pacing rules in the PPC budget calculator are specific to Google Ads."),
               ("Is my campaign data safe?", "Yes. All calculators run entirely in your browser. Your spend, revenue and costs are never uploaded or stored.")]),
    dict(slug='analytics-tools', short='UT', name='Analytics and Tracking Tools', pill='Analytics',
         card='UTM builders, GA4 event code, consent mode, regex tester and A/B test sample size.',
         hub_title='Free Analytics Tools: UTM Builder, GA4 and Tracking',
         hub_desc='Free analytics and tracking tools: UTM builder, bulk UTM links, GA4 event code, consent mode v2 code, GA4 regex tester and A/B test sample size calculator.',
         hub_lead='Build clean campaign links, generate tracking code and test filters for Google Analytics 4, all in your browser.',
         hub_intro=f'''<h2>Which Analytics Tool Do You Need?</h2>
    <ul>
      <li><strong>Tagging a campaign link?</strong> Use the <a href="{AN}utm-builder/">UTM Builder</a>, or the <a href="{AN}bulk-utm-builder/">Bulk UTM Builder</a> for many pages and channels at once.</li>
      <li><strong>Sharing a link full of tracking codes?</strong> Clean it with the <a href="{AN}utm-parameter-remover/">UTM Parameter Remover</a>.</li>
      <li><strong>Tracking leads, sign ups or sales?</strong> Write the code with the <a href="{AN}ga4-event-generator/">GA4 Event Code Generator</a>.</li>
      <li><strong>Serving visitors in Europe?</strong> Set up Google tags correctly with the <a href="{AN}consent-mode-v2-generator/">Consent Mode v2 Generator</a>.</li>
      <li><strong>Filtering reports?</strong> Check your pattern in the <a href="{AN}ga4-regex-tester/">GA4 Regex Tester</a> before you save it.</li>
      <li><strong>Planning an experiment?</strong> Work out visitors and days with the <a href="{AN}ab-test-sample-size-calculator/">A/B Test Sample Size Calculator</a>.</li>
    </ul>
    <p>Every tool follows Google's current GA4 documentation and checks your input as you type, so you catch problems before they reach your reports.</p>
    <p>New to campaign tracking? Read <a href="https://brandella.in/utm-parameters-explained/">UTM parameters explained</a> and <a href="https://brandella.in/google-analytics-4-metrics-explained-beginners/">GA4 metrics explained for beginners</a>.</p>''',
         faqs=[("Are these analytics tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do I need a Google Analytics account to use them?", "No. The tools build links and code you can use anywhere. You only need GA4 or Google Tag Manager when you put the code or links to work."),
               ("Is my data safe?", "Yes. All tools run entirely in your browser. URLs, event names and numbers you enter are never uploaded or stored.")]),
    dict(slug='social-media-tools', short='SM', name='Social Media Tools', pill='Social',
         card='Image resizer, link previews, character counter, bold text, WhatsApp links, engagement rate and YouTube chapters.',
         hub_title='Free Social Media Tools: Previews, Counters and Sizes',
         hub_desc='Free social media tools: image resizer, Open Graph preview, character counter, bold text, WhatsApp link generator, engagement rate and YouTube chapters.',
         hub_lead='Resize, preview, count and format your posts for Instagram, Facebook, LinkedIn, X, YouTube and WhatsApp before you publish.',
         hub_intro=f'''<h2>Which Social Media Tool Do You Need?</h2>
    <ul>
      <li><strong>Posting a photo?</strong> Crop it to the exact size with the <a href="{SMU}social-media-image-resizer/">Social Media Image Resizer</a>.</li>
      <li><strong>Sharing a link?</strong> See the card each app will show with the <a href="{SMU}open-graph-preview/">Open Graph Preview</a>.</li>
      <li><strong>Writing a caption or post?</strong> Check every limit at once with the <a href="{SMU}social-media-character-counter/">Social Media Character Counter</a>.</li>
      <li><strong>Want words to stand out?</strong> Add bold and italic with the <a href="{SMU}bold-text-generator/">Bold Text Generator</a>.</li>
      <li><strong>Getting leads on WhatsApp?</strong> Make a click to chat link with the <a href="{SMU}whatsapp-link-generator/">WhatsApp Link Generator</a>.</li>
      <li><strong>Reporting results?</strong> Work out your numbers with the <a href="{SMU}engagement-rate-calculator/">Engagement Rate Calculator</a>.</li>
      <li><strong>Uploading a video?</strong> Build valid timestamps with the <a href="{SMU}youtube-chapters-generator/">YouTube Chapters Generator</a>.</li>
    </ul>
    <p>Every tool follows the current rules published by each platform, such as X's character counting and YouTube's chapter requirements, and checks your work as you type.</p>
    <p>Planning your social content? Read our <a href="https://brandella.in/instagram-marketing-guide-businesses/">Instagram marketing guide</a> and <a href="https://brandella.in/social-media-kpis-every-marketer-should-track/">social media KPIs every marketer should track</a>.</p>''',
         faqs=[("Are these social media tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do I need to log in to my social accounts?", "No. The tools never connect to your accounts. You copy the result and paste it into the app yourself."),
               ("Is my data safe?", "Yes. All tools run entirely in your browser. Photos, posts and phone numbers you enter are never uploaded or stored.")]),
    dict(slug='technical-seo-tools', short='TS', name='Technical SEO Tools', pill='Technical SEO',
         card='Robots.txt generator and tester, XML sitemaps, hreflang tags and htaccess redirects.',
         hub_title='Free Technical SEO Tools: Robots.txt, Sitemaps, Hreflang',
         hub_desc='Free technical SEO tools: robots.txt generator and tester, XML sitemap generator and validator, hreflang generator and checker, and htaccess redirects.',
         hub_lead='Generate and test the technical files and tags that control how search engines crawl and index your site.',
         hub_intro=f'''<h2>Which Technical SEO Tool Do You Need?</h2>
    <ul>
      <li><strong>Controlling crawlers and AI bots?</strong> Write your file with the <a href="{TS}robots-txt-generator/">Robots.txt Generator</a>, then check URLs with the <a href="{TS}robots-txt-tester/">Robots.txt Tester</a>.</li>
      <li><strong>Helping Google find your pages?</strong> Build a file with the <a href="{TS}xml-sitemap-generator/">XML Sitemap Generator</a> and check an existing one with the <a href="{TS}xml-sitemap-validator/">XML Sitemap Validator</a>.</li>
      <li><strong>Running a site in several languages or countries?</strong> Create tags with the <a href="{TS}hreflang-tag-generator/">Hreflang Tag Generator</a> and audit them with the <a href="{TS}hreflang-checker/">Hreflang Checker</a>.</li>
      <li><strong>Changing URLs or moving to HTTPS?</strong> Create 301 rules with the <a href="{TS}htaccess-redirect-generator/">Htaccess Redirect Generator</a>.</li>
    </ul>
    <p>Every tool follows Google's current documentation for robots.txt, sitemaps, hreflang and redirects, and checks your work as you type.</p>
    <p>New to technical SEO? Read <a href="https://brandella.in/how-google-crawls-websites/">how Google crawls websites</a> and <a href="https://brandella.in/crawl-budget-explained/">crawl budget explained</a>.</p>''',
         faqs=[("Are these technical SEO tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do the tools crawl or fetch my website?", "No. You paste your file, list or tags and everything is checked inside your browser. That also means the tools work on staging sites that are not public yet."),
               ("Is my data safe?", "Yes. Nothing you paste is uploaded or stored. URLs, robots.txt files and sitemaps stay on your device.")]),
    dict(slug='google-ads-tools', short='GA', name='Google Ads Tools', pill='Google Ads',
         card='Ad preview, character counter, match types, negative keywords, ngram analysis, tracking templates and keyword grouping.',
         hub_title='Free Google Ads Tools: Ad Preview, Keywords and Tracking',
         hub_desc='Free Google Ads tools: ad preview, character counter, match type generator, negative keyword tool, ngram analyzer, tracking templates and keyword grouper.',
         hub_lead='Write, preview and organise Google Ads campaigns faster, with tools that follow the platform\'s real limits and rules.',
         hub_intro=f'''<h2>Which Google Ads Tool Do You Need?</h2>
    <ul>
      <li><strong>Writing a new ad?</strong> See it as a real result with the <a href="{GA}google-ads-preview-tool/">Google Ads Preview Tool</a> and check every asset with the <a href="{GA}google-ads-character-counter/">Google Ads Character Counter</a>.</li>
      <li><strong>Building keyword lists?</strong> Sort them into ad groups with the <a href="{GA}keyword-grouper/">Keyword Grouper</a>, then add quotes and brackets with the <a href="{GA}keyword-match-type-generator/">Keyword Match Type Generator</a>.</li>
      <li><strong>Cutting wasted spend?</strong> Find costly words with the <a href="{GA}search-term-ngram-analyzer/">Search Term Ngram Analyzer</a> and test your list in the <a href="{GA}negative-keyword-tool/">Negative Keyword Tool</a>.</li>
      <li><strong>Setting up tracking?</strong> Create UTM tags and ValueTrack parameters with the <a href="{GA}google-ads-tracking-template-generator/">Google Ads Tracking Template Generator</a>.</li>
    </ul>
    <p>Every tool follows Google's current help pages for responsive search ads, keyword match types, negative keywords and ValueTrack, and checks your work as you type.</p>
    <p>New to paid search? Read <a href="https://brandella.in/how-google-ads-auction-works/">how the Google Ads auction works</a> and our guide to <a href="https://brandella.in/google-ads-negative-keywords/">Google Ads negative keywords</a>.</p>''',
         faqs=[("Are these Google Ads tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do I need to connect my Google Ads account?", "No. The tools never log in to Google Ads. You paste your text, keywords or reports, then copy the result back into Google Ads or Google Ads Editor."),
               ("Is my campaign data safe?", "Yes. All tools run entirely in your browser. Ad copy, keywords, costs and search terms you paste are never uploaded or stored.")]),
    dict(slug='ai-tools', short='AI', name='AI Tools', pill='AI',
         card='llms.txt generator, AI crawler log analyzer, token counter, prompt generator, AI text cleaner and Markdown converters.',
         hub_title='Free AI Tools for Marketers: llms.txt, Prompts and Tokens',
         hub_desc='Free AI tools for marketers: llms.txt generator, AI crawler log analyzer, token counter, prompt generator, AI text cleaner and Markdown converters.',
         hub_lead='Practical tools for the AI search era: get found by AI assistants, write better prompts and clean up AI written text, all in your browser.',
         hub_intro=f'''<h2>Which AI Tool Do You Need?</h2>
    <ul>
      <li><strong>Want AI assistants to find your best pages?</strong> Build a file with the <a href="{AI}llms-txt-generator/">llms.txt Generator</a>.</li>
      <li><strong>Wondering if GPTBot or ClaudeBot visit you?</strong> Paste your server log into the <a href="{AI}ai-crawler-log-analyzer/">AI Crawler Log Analyzer</a>.</li>
      <li><strong>Getting vague answers from ChatGPT?</strong> Structure your request with the <a href="{AI}ai-prompt-generator/">AI Prompt Generator</a>.</li>
      <li><strong>Working with long documents or the API?</strong> Check size, cost and chunks with the <a href="{AI}ai-token-counter/">AI Token Counter</a>.</li>
      <li><strong>Publishing AI assisted text?</strong> Strip hidden characters and filler with the <a href="{AI}ai-text-cleaner/">AI Text Cleaner</a>, or keep the formatting with the <a href="{AI}markdown-to-html-converter/">Markdown to HTML Converter</a>.</li>
      <li><strong>Feeding a web page to an AI?</strong> Shrink it first with the <a href="{AI}html-to-markdown-converter/">HTML to Markdown Converter</a>.</li>
    </ul>
    <p>Every tool runs entirely in your browser. Nothing you paste is sent to an AI model, to us or to anyone else.</p>
    <p>New to AI search? Read <a href="https://brandella.in/aeo-vs-seo-vs-geo-difference-2026/">AEO vs SEO vs GEO</a> and our guide on <a href="https://brandella.in/how-to-increase-ai-search-citations/">how to increase AI search citations</a>.</p>''',
         faqs=[("Are these AI tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do these tools send my text to ChatGPT or another AI?", "No. They do not call any AI model or API. Prompts, logs and text you paste are processed in your browser and never leave your device."),
               ("Will llms.txt or these tools improve my Google rankings?", "Not directly. Google says its search features do not use llms.txt. The tools help you understand AI crawlers, write better prompts and publish cleaner content, which supports visibility in AI assistants and search alike.")]),
    dict(slug='developer-tools', short='DEV', name='Developer Tools', pill='Developer',
         card='JSON formatter, URL encoder, diff checker, Base64 and JWT decoder, Unix timestamp converter and CSV to JSON converter.',
         hub_title='Free Developer Tools: JSON Formatter, CSV to JSON and More',
         hub_desc='Free online developer tools: JSON formatter, URL encoder, diff checker, Base64 and JWT decoder, Unix timestamp converter and CSV to JSON converter.',
         hub_lead='Everyday web developer utilities that run instantly in your browser, with nothing uploaded to a server.',
         hub_intro=f'''<h2>Which Developer Tool Do You Need?</h2>
    <ul>
      <li><strong>Reading an API response or fixing broken JSON from an AI tool?</strong> Use the <a href="{DV}json-formatter/">JSON Formatter and Validator</a>.</li>
      <li><strong>Checking a tracking link or building a redirect URL?</strong> Use the <a href="{DV}url-encoder-decoder/">URL Encoder and Decoder</a>.</li>
      <li><strong>Want to see what changed between two versions, or what an AI edit really did?</strong> Use the <a href="{DV}diff-checker/">Diff Checker</a>.</li>
      <li><strong>Reading a JWT token or turning an image into a data URI?</strong> Use the <a href="{DV}base64-encoder-decoder/">Base64 Encoder and Decoder</a>.</li>
      <li><strong>Got an epoch time in a log, API or GA4 export?</strong> Turn it into a real date with the <a href="{DV}unix-timestamp-converter/">Unix Timestamp Converter</a>.</li>
      <li><strong>Moving data between a spreadsheet and code or an AI batch file?</strong> Use the <a href="{DV}csv-to-json-converter/">CSV to JSON Converter</a>, which also turns JSON back into CSV.</li>
    </ul>
    <p>Every tool follows the official standards, such as RFC 8259 for JSON, RFC 3986 for URLs, RFC 4648 for Base64 and RFC 4180 for CSV, and gives the same result your code would. More developer tools are added regularly.</p>
    <p>Building something yourself? Read <a href="https://brandella.in/rest-api-in-php-without-a-framework/">how to build a REST API in PHP</a> and <a href="https://brandella.in/gtm-data-layer-explained/">the GTM data layer explained</a>.</p>''',
         faqs=[("Are these developer tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Is my code or data uploaded anywhere?", "No. All tools run entirely in your browser. JSON, URLs, tokens, files and text you paste never leave your device, so it is safe to use them with private API data."),
               ("Do the tools work offline?", "Once a tool page has loaded, it keeps working without a connection, because all the processing happens in your browser.")],
         app_category='DeveloperApplication'),
    dict(slug='email-marketing-tools', short='EM', name='Email Marketing Tools', pill='Email',
         card='Email subject line tester, email list cleaner, email header analyzer, and SPF, DKIM and DMARC record generators.',
         hub_title='Free Email Marketing Tools: List Cleaner, SPF, DKIM, DMARC',
         hub_desc='Free email marketing tools: subject line tester, email list cleaner, email header analyzer, and SPF, DKIM and DMARC record generators. All in your browser.',
         hub_lead='Write subject lines that get opened, clean your list, and set up your domain so your emails reach the inbox.',
         hub_intro=f'''<h2>Which Email Tool Do You Need?</h2>
    <ul>
      <li><strong>Writing a campaign?</strong> Score your subject line and preheader with the <a href="{EM}email-subject-line-tester/">Email Subject Line Tester</a>, and rank several ideas at once.</li>
      <li><strong>Importing a new list?</strong> Remove duplicates, typos, broken and throwaway addresses with the <a href="{EM}email-list-cleaner/">Email List Cleaner</a>, then download a clean CSV.</li>
      <li><strong>Email landed in spam or arrived late?</strong> Paste its headers into the <a href="{EM}email-header-analyzer/">Email Header Analyzer</a> to see SPF, DKIM and DMARC results and every delivery hop.</li>
      <li><strong>Adding a new email service, or seeing SPF errors?</strong> Combine every sender into one record, count DNS lookups and merge duplicates with the <a href="{EM}spf-record-generator/">SPF Record Generator and Checker</a>.</li>
      <li><strong>Running your own mail server or Amazon SES?</strong> Create a private key and the matching TXT record, or check an existing record and its key size, with the <a href="{EM}dkim-record-generator/">DKIM Record Generator and Checker</a>.</li>
      <li><strong>Emails landing in spam, or sending to Gmail in bulk?</strong> Build or check your record with the <a href="{EM}dmarc-record-generator/">DMARC Record Generator and Checker</a>.</li>
    </ul>
    <p>Every tool follows current mailbox rules, such as the Google email sender guidelines, RFC 7208 for SPF, RFC 6376 and RFC 8301 for DKIM, RFC 9989 for DMARC and RFC 8601 for authentication results, and runs entirely in your browser. More email tools are added regularly.</p>
    <p>Planning your emails? Read our <a href="https://brandella.in/email-marketing-strategy/">email marketing strategy guide</a> and <a href="https://brandella.in/how-to-generate-high-quality-leads-2026/">how to generate high quality leads</a>.</p>''',
         faqs=[("Are these email marketing tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do you see my subject lines, lists or domain settings?", "No. All tools run entirely in your browser. Subject lines, records and email lists you enter never leave your device."),
               ("Do these tools send test emails?", "No. They check and build things in your browser without sending any email, so nothing reaches your list by accident.")]),
    dict(slug='content-writing-tools', short='CW', name='Content Writing Tools', pill='Content',
         card='Headline analyzer, AI words checker and text similarity checker: score titles, fix ChatGPT words and catch copied text.',
         hub_title='Free Content Writing Tools: Headlines, AI Words, Similarity',
         hub_desc='Free content writing tools: headline analyzer, AI words checker for overused ChatGPT words, and a text similarity checker to compare two texts.',
         hub_lead='Small, focused tools that help you plan, write and polish content faster.',
         hub_intro=f'''<h2>Which Writing Tool Do You Need?</h2>
    <ul>
      <li><strong>Choosing a title for a post, page or video?</strong> Score it and rank several ideas with the <a href="{CW}headline-analyzer/">Headline Analyzer</a>.</li>
      <li><strong>Editing a draft written with ChatGPT or another AI?</strong> Find words like delve and testament, and swap them for plain English, with the <a href="{CW}ai-words-checker/">AI Words Checker</a>.</li>
      <li><strong>Checking a rewrite, guest post or essay for copying?</strong> Compare it with the source and see every shared passage in the <a href="{CW}text-similarity-checker/">Text Similarity Checker</a>.</li>
      <li><strong>Checking how easy your text is to read?</strong> Use the <a href="{H}readability-score-checker/">Readability Score Checker</a>.</li>
      <li><strong>Counting words or formatting a title?</strong> Try the <a href="{H}word-character-counter/">Word and Character Counter</a> and the <a href="{H}title-case-converter/">Title Case Converter</a>.</li>
      <li><strong>Publishing AI assisted text?</strong> Strip hidden characters and filler with the <a href="{AI}ai-text-cleaner/">AI Text Cleaner</a>.</li>
    </ul>
    <p>Every tool follows Google's current guidance on titles and helpful content, and runs entirely in your browser. More writing tools are added regularly.</p>
    <p>Want to write better? Read <a href="https://brandella.in/10-easy-tips-for-effective-content-writing/">10 easy tips for effective content writing</a> and <a href="https://brandella.in/25-content-writing-mistakes/">25 content writing mistakes</a>.</p>''',
         faqs=[("Are these content writing tools free?", "Yes. Every tool is free, needs no signup, and has no usage limits."),
               ("Do these tools use AI or send my text anywhere?", "No. They do not call any AI model or server. Headlines, drafts and texts you compare are checked in your browser and never leave your device."),
               ("Will a higher headline score guarantee more clicks?", "No tool can promise that. The score points out common problems, such as length, clickbait and missing keywords, so you start from a stronger headline. Your own click data is the final test.")]),
    dict(slug='business-calculators', short='BC', name='Business Calculators', pill='Business',
         card='Marketing ROI, customer lifetime value, CRO and pricing calculators.',
         hub_title='Free Marketing Business Calculators: ROI, CLV and More',
         hub_desc='Free business calculators for marketers: marketing ROI, customer lifetime value, CAC, conversion rate uplift, GST and pricing.',
         hub_lead='Turn marketing numbers into business decisions with simple, clear calculators.'),
]
