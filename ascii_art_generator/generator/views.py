from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AsciiArt
from .forms import AsciiArtForm
from PIL import Image
import os
import base64
from io import BytesIO

# ASCII characters ordered by increasing "density"
ASCII_CHARS = ' .,:;i1tfLCG08@'

def convert_image_to_ascii(image_path, width=100):
    """
    Convert an image to ASCII art
    
    Args:
        image_path: Path to the image file
        width: Width of the ASCII art in characters
        
    Returns:
        ASCII art as a string
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Calculate dimensions
        aspect_ratio = image.height / image.width
        new_width = width
        new_height = int(aspect_ratio * new_width * 0.55)  # Adjustment for character aspect ratio
        
        # Resize the image
        image = image.resize((new_width, new_height))
        
        # Convert to grayscale
        image = image.convert("L")
        
        # Convert pixels to ASCII
        pixels = list(image.getdata())
        ascii_str = ''.join([ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels])
        
        # Format with line breaks
        ascii_art = '\n'.join(ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width))
        
        return ascii_art
        
    except Exception as e:
        return f"Error processing image: {e}"

def home(request):
    """Homepage view"""
    recent_arts = AsciiArt.objects.order_by('-created_at')[:3]
    return render(request, 'generator/home.html', {'recent_arts': recent_arts})

def generate_ascii(request):
    """View for generating ASCII art"""
    if request.method == 'POST':
        form = AsciiArtForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an instance but don't assign ASCII yet
            ascii_art = form.save(commit=False)

            # Associate with user if logged in
            if request.user.is_authenticated:
                ascii_art.user = request.user

            # Save once to store uploaded image to disk
            ascii_art.save()

            # Get the width from the form
            width = form.cleaned_data.get('width', 100)

            # Now safely access the image path
            image_path = ascii_art.original_image.path

            # Convert the image to ASCII
            ascii_result = convert_image_to_ascii(image_path, width)
            ascii_art.ascii_result = ascii_result

            # Save again to store ASCII result
            ascii_art.save()

            return redirect('view_result', pk=ascii_art.pk)
    else:
        form = AsciiArtForm()

    return render(request, 'generator/generate.html', {'form': form})

def view_result(request, pk):
    """View for displaying a specific ASCII art result"""
    ascii_art = get_object_or_404(AsciiArt, pk=pk)
    
    # Convert image to base64 for display
    with open(ascii_art.original_image.path, 'rb') as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')
    
    context = {
        'ascii_art': ascii_art,
        'original_image': image_data,
    }
    return render(request, 'generator/result.html', context)

@login_required
def my_gallery(request):
    """View for user's gallery of ASCII arts"""
    user_arts = AsciiArt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'generator/gallery.html', {'arts': user_arts})

def gallery(request):
    """View for public gallery of ASCII arts"""
    arts = AsciiArt.objects.order_by('-created_at')
    return render(request, 'generator/gallery.html', {'arts': arts})

@login_required
def delete_art(request, pk):
    """View for deleting ASCII art"""
    ascii_art = get_object_or_404(AsciiArt, pk=pk)
    
    # Check if the user owns this ASCII art
    if ascii_art.user != request.user:
        messages.error(request, "You don't have permission to delete this.")
        return redirect('view_result', pk=pk)
    
    # Delete the ASCII art
    ascii_art.delete()
    messages.success(request, "ASCII art deleted successfully.")
    return redirect('my_gallery')