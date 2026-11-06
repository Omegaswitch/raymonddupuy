# source/original

Deliberately not populated with King's book (rights status unverified; the PDF is 175 MB). To reproduce:

```bash
curl -L -o king.pdf "https://archive.org/download/king-rule-statutes-and-customs-of-the-hospitallers/King%20Rule%20Statutes%20and%20Customs%20of%20the%20Hospitallers.pdf"
sha256sum king.pdf   # expect 5741ebc3473b3ffee670cd4823c46804d97a2a2dff50a71e7d3d86fd6d730843
pdftoppm -r 90 -f 40 -l 50 -png king.pdf p   # PDF page = book page + 20 for pp. 22–28; plates occupy PDF pp. 41–42
```
Book pp. 20–28 = PDF pages 40, 43–50 (PDF 41–42 are un-numbered plates).
