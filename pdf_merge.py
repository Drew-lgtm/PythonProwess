from pypdf import PdfWriter


def merge_pdfs(input_files, output_filename):
    writer = PdfWriter()

    for pdf in input_files:
        try:
            # Append the entire PDF file to the writer
            writer.append(pdf)
            print(f"Successfully added: {pdf}")
        except FileNotFoundError:
            print(f"Error: {pdf} not found.")
        except Exception as e:
            print(f"Error processing {pdf}: {e}")

    # Write the merged PDF to the specified output file
    with open(output_filename, "wb") as output_file:
        writer.write(output_file)

    print(f"Merged PDF saved as: {output_filename}")


# Configuration
files_to_merge = ["document1.pdf", "document2.pdf"]
output_name = "merged_result.pdf"

if __name__ == "__main__":
    merge_pdfs(files_to_merge, output_name)
