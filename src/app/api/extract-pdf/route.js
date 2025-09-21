import pdfParse from 'pdf-parse';
import { NextResponse } from 'next/server';

// Custom helper to handle form data (without multer)
export async function POST(req) {
  const formData = await req.formData();
  const file = formData.get('pdf');

  if (!file) {
    return NextResponse.json({ error: 'No PDF file provided' }, { status: 400 });
  }

  const arrayBuffer = await file.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);

  try {
    const data = await pdfParse(buffer);
    return NextResponse.json({ text: data.text });
  } catch (error) {
    console.error('PDF parsing failed:', error);
    return NextResponse.json({ error: 'Failed to parse PDF' }, { status: 500 });
  }
}
