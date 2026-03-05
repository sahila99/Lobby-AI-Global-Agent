print("Hello World")
import asyncio
import aiohttp
import json
from playwright.async_api import async_playwright
from datetime import datetime
from typing import List, Dict


class JobScraper:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.jobs = []
        self.sources = {
            "naukri_gulf": "https://www.naukri.com/jobs-in-gulf/product-manager-jobs",
            "naukri_india": "https://www.naukri.com/jobs-in-india/product-manager-jobs",
            "michael_page": "https://www.michaelpage.com/jobs/product-manager",
            "randstad": "https://www.randstad.com/jobs/search/?q=product-manager"
        }
        self.countries_map = {
            "naukri_gulf": ["UAE", "UK", "Germany"],
            "naukri_india": ["India"],
            "michael_page": ["UAE", "UK", "Germany", "Africa"],
            "randstad": ["UAE", "UK", "Germany", "Africa"]
        }

    async def run(self) -> Dict:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()

                await self.scrape_naukri_gulf(context)
                await self.scrape_naukri_india(context)
                await self.scrape_michael_page(context)
                await self.scrape_randstad(context)

                await context.close()
                await browser.close()

            result = await self.send_to_webhook()
            return result
        except Exception as e:
            print(f"Scraper error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'jobs_found': 0,
                'webhook_sent': False
            }

    async def scrape_naukri_gulf(self, context):
        try:
            page = await context.new_page()
            await page.goto(self.sources["naukri_gulf"], wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            job_elements = await page.query_selector_all('[data-job-id]')
            for element in job_elements[:10]:
                try:
                    title = await element.query_selector('.title')
                    company = await element.query_selector('.companyName')
                    description_elem = await element.query_selector('.description')

                    if title and company:
                        job_data = {
                            'title': (await title.text_content()).strip(),
                            'company': (await company.text_content()).strip(),
                            'country': 'UAE',
                            'description': (await description_elem.text_content()).strip() if description_elem else '',
                            'source': 'Naukri Gulf'
                        }
                        self.jobs.append(job_data)
                except:
                    continue

            await page.close()
        except Exception as e:
            print(f"Naukri Gulf scrape error: {str(e)}")

    async def scrape_naukri_india(self, context):
        try:
            page = await context.new_page()
            await page.goto(self.sources["naukri_india"], wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            job_elements = await page.query_selector_all('[data-job-id]')
            for element in job_elements[:10]:
                try:
                    title = await element.query_selector('.title')
                    company = await element.query_selector('.companyName')
                    description_elem = await element.query_selector('.description')

                    if title and company:
                        job_data = {
                            'title': (await title.text_content()).strip(),
                            'company': (await company.text_content()).strip(),
                            'country': 'India',
                            'description': (await description_elem.text_content()).strip() if description_elem else '',
                            'source': 'Naukri India'
                        }
                        self.jobs.append(job_data)
                except:
                    continue

            await page.close()
        except Exception as e:
            print(f"Naukri India scrape error: {str(e)}")

    async def scrape_michael_page(self, context):
        try:
            page = await context.new_page()
            await page.goto(self.sources["michael_page"], wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            job_elements = await page.query_selector_all('.job-card, [class*="job"]')
            for element in job_elements[:15]:
                try:
                    title = await element.query_selector('h2, [class*="title"]')
                    company = await element.query_selector('[class*="company"]')
                    location = await element.query_selector('[class*="location"]')
                    description = await element.query_selector('[class*="description"]')

                    if title and company:
                        country = self._extract_country(location)
                        job_data = {
                            'title': (await title.text_content()).strip(),
                            'company': (await company.text_content()).strip(),
                            'country': country,
                            'description': (await description.text_content()).strip() if description else '',
                            'source': 'Michael Page'
                        }
                        self.jobs.append(job_data)
                except:
                    continue

            await page.close()
        except Exception as e:
            print(f"Michael Page scrape error: {str(e)}")

    async def scrape_randstad(self, context):
        try:
            page = await context.new_page()
            await page.goto(self.sources["randstad"], wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            job_elements = await page.query_selector_all('[data-test*="job"], .job-item, [class*="job-card"]')
            for element in job_elements[:15]:
                try:
                    title = await element.query_selector('h2, h3, [class*="title"]')
                    company = await element.query_selector('[class*="company"], [class*="employer"]')
                    location = await element.query_selector('[class*="location"]')
                    description = await element.query_selector('[class*="description"]')

                    if title and company:
                        country = self._extract_country(location)
                        job_data = {
                            'title': (await title.text_content()).strip(),
                            'company': (await company.text_content()).strip(),
                            'country': country,
                            'description': (await description.text_content()).strip() if description else '',
                            'source': 'Randstad'
                        }
                        self.jobs.append(job_data)
                except:
                    continue

            await page.close()
        except Exception as e:
            print(f"Randstad scrape error: {str(e)}")

    def _extract_country(self, location_element) -> str:
        if not location_element:
            return "Unknown"

        location_text = location_element.text_content() if hasattr(location_element, 'text_content') else str(location_element)
        location_lower = location_text.lower()

        countries = {
            'uae': 'UAE',
            'dubai': 'UAE',
            'abu dhabi': 'UAE',
            'uk': 'UK',
            'london': 'UK',
            'germany': 'Germany',
            'berlin': 'Germany',
            'frankfurt': 'Germany',
            'africa': 'Africa',
            'south africa': 'Africa',
            'nigeria': 'Africa',
            'kenya': 'Africa',
            'india': 'India',
            'bangalore': 'India',
            'mumbai': 'India',
            'delhi': 'India'
        }

        for key, country in countries.items():
            if key in location_lower:
                return country

        return "Unknown"

    async def send_to_webhook(self) -> Dict:
        try:
            payload = {
                'jobs': self.jobs,
                'total_count': len(self.jobs),
                'timestamp': datetime.now().isoformat(),
                'sources': list(set([job['source'] for job in self.jobs]))
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    webhook_sent = response.status in [200, 201, 202]

            return {
                'success': True,
                'jobs_found': len(self.jobs),
                'webhook_sent': webhook_sent,
                'message': f'Successfully scraped {len(self.jobs)} jobs and sent to webhook'
            }
        except Exception as e:
            print(f"Webhook error: {str(e)}")
            return {
                'success': True,
                'jobs_found': len(self.jobs),
                'webhook_sent': False,
                'message': f'Scraped {len(self.jobs)} jobs but webhook delivery failed: {str(e)}'
            }
async def main():
    # This is your secret webhook URL
    url = "https://hook.eu1.make.com/yqy3wmxomg9e5536qiokz0kja3vwgart"
    
    print("🚀 Starting the Global Job Scout...")
    scraper = JobScraper(url)
    result = await scraper.run()
    
    print("-" * 30)
    print(f"✅ Status: {result['message']}")
    print(f"📊 Total Jobs Found: {result['jobs_found']}")
    print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())
