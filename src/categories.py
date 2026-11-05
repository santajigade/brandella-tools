"""Tool categories. A category goes live automatically once it has at least one tool.
Order here = order on /tools/. Slugs are permanent URLs: never rename a live one."""

H = 'https://brandella.in/tools/seo-tools/'
S = 'https://brandella.in/tools/schema-generators/'
PP = 'https://brandella.in/tools/ppc-calculators/'
AN = 'https://brandella.in/tools/analytics-tools/'
SMU = 'https://brandella.in/tools/social-media-tools/'
TS = 'https://brandella.in/tools/technical-seo-tools/'
GA = 'https://brandella.in/tools/google-ads-tools/'

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
         card='llms.txt generator, AI crawler checker, token counter, prompt builder and AI text cleaner.',
         hub_title='Free AI Tools for Marketers: llms.txt, Prompts and Tokens',
         hub_desc='Free AI tools for marketers: llms.txt generator, AI crawler checker, token counter, prompt builder and AI text cleaner. Private and browser based.',
         hub_lead='Practical tools for the AI search era: get found by AI assistants, write better prompts and clean up AI written text, all in your browser.'),
    dict(slug='developer-tools', short='DEV', name='Developer Tools', pill='Developer',
         card='JSON formatter, HTML and CSS minifier, Base64, URL encoder and more.',
         hub_title='Free Developer Tools: JSON Formatter, Minifiers and More',
         hub_desc='Free online developer tools: JSON formatter and validator, HTML, CSS and JS minifier, Base64 and URL encoder, regex tester and more.',
         hub_lead='Everyday web developer utilities that run instantly in your browser, with nothing uploaded to a server.',
         app_category='DeveloperApplication'),
    dict(slug='email-marketing-tools', short='EM', name='Email Marketing Tools', pill='Email',
         card='Subject line tester, preheader preview and signature generator.',
         hub_title='Free Email Marketing Tools: Subject Lines and Signatures',
         hub_desc='Free email marketing tools: subject line tester, inbox preview, email signature generator, spam word checker and more. No signup needed.',
         hub_lead='Write subject lines that get opened, preview your inbox listing and build a professional email signature.'),
    dict(slug='content-writing-tools', short='CW', name='Content Writing Tools', pill='Content',
         card='Headline analyzer, outline builder and writing helpers.',
         hub_title='Free Content Writing Tools: Headlines, Outlines and More',
         hub_desc='Free content writing tools: headline analyzer, blog outline generator, lorem ipsum, text cleaner and more to write faster and better.',
         hub_lead='Small, focused tools that help you plan, write and polish content faster.'),
    dict(slug='business-calculators', short='BC', name='Business Calculators', pill='Business',
         card='Marketing ROI, customer lifetime value, CRO and pricing calculators.',
         hub_title='Free Marketing Business Calculators: ROI, CLV and More',
         hub_desc='Free business calculators for marketers: marketing ROI, customer lifetime value, CAC, conversion rate uplift, GST and pricing.',
         hub_lead='Turn marketing numbers into business decisions with simple, clear calculators.'),
]
