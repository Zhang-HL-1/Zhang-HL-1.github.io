import json
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
import build


class BuildTest(unittest.TestCase):
    def test_publish_search_feed_and_draft(self):
        root, out = build.ROOT, build.OUT
        with tempfile.TemporaryDirectory() as directory:
            try:
                build.ROOT = Path(directory)
                build.OUT = build.ROOT / 'docs'
                shutil.copytree(root / 'site', build.ROOT / 'site')
                content = build.ROOT / 'content/posts'
                content.mkdir(parents=True)
                template = '---\ntitle: 电路 & 信号\ndate: 2026-10-23\ncategory: 技术笔记\ndescription: 测试摘要\ndraft: %s\n---\n\n## 节点分析\n\n关键词 **电压**\n\n```python\nprint(1)\n```\n'
                (content / 'circuit.md').write_text(template % 'false', encoding='utf-8')
                (content / 'draft.md').write_text(template % 'true', encoding='utf-8')
                build.build()
                posts = json.loads((build.OUT / 'posts.json').read_text())
                self.assertEqual(len(posts), 1)
                self.assertIn('电压', posts[0]['text'])
                page = (build.OUT / 'posts/circuit/index.html').read_text()
                self.assertIn('<strong>电压</strong>', page)
                self.assertIn('电路 &amp; 信号', page)
                self.assertFalse((build.OUT / 'posts/draft').exists())
                self.assertEqual(len(ET.parse(build.OUT / 'rss.xml').findall('.//item')), 1)
                ET.parse(build.OUT / 'sitemap.xml')
                (content / 'circuit.md').unlink()
                build.build()
                self.assertFalse((build.OUT / 'posts/circuit').exists())
                self.assertEqual(json.loads((build.OUT / 'posts.json').read_text()), [])
            finally:
                build.ROOT, build.OUT = root, out


if __name__ == '__main__':
    unittest.main()
