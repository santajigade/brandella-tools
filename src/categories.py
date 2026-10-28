"""Tool categories. A category goes live automatically once it has at least one tool.
Order here = order on /tools/. Slugs are permanent URLs: never rename a live one."""

H = 'https://brandella.in/tools/seo-tools/'

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
         card='FAQ, LocalBusiness, Article, Product, HowTo and Organization JSON LD.',
         hub_title='Free Schema Markup Generators: JSON LD for Google',
         hub_desc='Free schema markup generators for FAQ, LocalBusiness, Article, Product, Organization and more. Create valid JSON LD for rich results in seconds.',
         hub_lead='Create valid JSON LD schema markup for rich results in seconds. Fill in a form, copy the code, and paste it into your page.'),
    dict(slug='ppc-calculators', short='PPC', name='PPC Calculators', pill='PPC',
         card='ROAS, CPA, CPC, CTR, break even ROAS and ad budget calculators.',
         hub_title='Free PPC Calculators: ROAS, CPA, CPC, CTR and Budget',
         hub_desc='Free PPC calculators for ROAS, CPA, CPC, CTR, conversion rate, break even ROAS and ad budgets. Plan and evaluate Google and Meta campaigns.',
         hub_lead='Quick, accurate calculators for planning and judging paid campaigns on Google Ads, Meta, LinkedIn and more.'),
    dict(slug='analytics-tools', short='UT', name='Analytics and Tracking Tools', pill='Analytics',
         card='UTM builder, GA4 event code, regex tester and tracking helpers.',
         hub_title='Free Analytics Tools: UTM Builder, GA4 and Tracking',
         hub_desc='Free analytics and tracking tools: UTM link builder, GA4 event code generator, regex tester for filters, and more. No signup needed.',
         hub_lead='Build clean campaign links, generate tracking code and test filters for Google Analytics 4, all in your browser.'),
    dict(slug='social-media-tools', short='SM', name='Social Media Tools', pill='Social',
         card='Post previews, character counters, image sizes and hashtag tools.',
         hub_title='Free Social Media Tools: Previews, Counters and Sizes',
         hub_desc='Free social media tools: Open Graph preview, post character counters, image size guide, hashtag formatter and more for every major network.',
         hub_lead='Preview, size and format your posts for Facebook, Instagram, LinkedIn, X, YouTube and TikTok before you publish.'),
    dict(slug='technical-seo-tools', short='TS', name='Technical SEO Tools', pill='Technical SEO',
         card='Robots.txt, hreflang, XML sitemap, redirect and canonical tools.',
         hub_title='Free Technical SEO Tools: Robots.txt, Hreflang, Sitemaps',
         hub_desc='Free technical SEO tools: robots.txt generator and tester, hreflang generator, XML sitemap generator, htaccess redirects and more.',
         hub_lead='Generate and test the technical files and tags that control how search engines crawl and index your site.'),
    dict(slug='google-ads-tools', short='GA', name='Google Ads Tools', pill='Google Ads',
         card='Ad preview, character counter, match type and negative keyword tools.',
         hub_title='Free Google Ads Tools: Ad Preview, Counters and Keywords',
         hub_desc='Free Google Ads tools: responsive search ad preview, headline character counter, match type converter, negative keyword builder and more.',
         hub_lead='Write, preview and organise Google Ads campaigns faster, with tools that follow the platform\'s real limits.'),
    dict(slug='developer-tools', short='DEV', name='Developer Tools', pill='Developer',
         card='JSON formatter, HTML and CSS minifier, Base64, URL encoder and more.',
         hub_title='Free Developer Tools: JSON Formatter, Minifiers and More',
         hub_desc='Free online developer tools: JSON formatter and validator, HTML, CSS and JS minifier, Base64 and URL encoder, regex tester and more.',
         hub_lead='Everyday web developer utilities that run instantly in your browser, with nothing uploaded to a server.',
         app_category='DeveloperApplication'),
    dict(slug='ai-tools', short='AI', name='AI Tools', pill='AI',
         card='Prompt generators, llms.txt builder and AI token counters.',
         hub_title='Free AI Tools for Marketers: Prompts, llms.txt and More',
         hub_desc='Free AI tools for marketers: prompt generators, llms.txt builder, token counter and AI content helpers. Practical, private and browser based.',
         hub_lead='Practical AI helpers for marketers: better prompts, AI crawler files and quick checks, all running in your browser.'),
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
