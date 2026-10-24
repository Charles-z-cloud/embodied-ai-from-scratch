from pathlib import Path
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt


def correlate_valid(x, kernel):
    h, w = x.shape
    kh, kw = kernel.shape
    result = np.zeros((h - kh + 1, w - kw + 1), dtype=np.float32)
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            result[row, col] = np.sum(x[row:row + kh, col:col + kw] * kernel)
    return result


if __name__ == "__main__":
    torch.set_num_threads(1)
    folder = Path(__file__).resolve().parents[1] / "figures"
    folder.mkdir(exist_ok=True)
    pixels = np.full((64, 64, 3), 30, dtype=np.uint8)
    pixels[20:44, 16:40] = [240, 40, 40]
    pixels[8:20, 44:56] = [40, 40, 240]
    path = folder / "blocks.png"
    Image.fromarray(pixels).save(path)
    with Image.open(path) as picture:
        rgb = np.array(picture.convert("RGB"), dtype=np.float32) / 255
        resized = np.array(picture.resize((32, 32), resample=Image.Resampling.BILINEAR))
    tensor = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0)
    print("HWC / NCHW / resized:", rgb.shape, tuple(tensor.shape), resized.shape)
    assert np.allclose(rgb[20, 16], np.array([240, 40, 40]) / 255)
    gray = rgb.mean(axis=2)
    kernel = np.array([[1., -1.]], dtype=np.float32)
    edge = correlate_valid(gray, kernel)
    torch_edge = F.conv2d(torch.from_numpy(gray)[None, None], torch.from_numpy(kernel)[None, None])
    assert np.allclose(edge, torch_edge[0, 0].numpy(), atol=1e-6)
    small = np.arange(1, 10, dtype=np.float32).reshape(3, 3)
    hand_kernel = np.array([[1., 0.], [0., -1.]], dtype=np.float32)
    hand = correlate_valid(small, hand_kernel)
    print("hand convolution:\n", hand)
    assert np.array_equal(hand, np.full((2, 2), -4))
    print("edge shape / range:", edge.shape, edge.min(), edge.max())
    conv = torch.nn.Conv2d(3, 8, kernel_size=3, padding=1, stride=2)
    print("conv output / parameter count:", tuple(conv(tensor).shape), sum(p.numel() for p in conv.parameters()))
    assert tuple(conv(tensor).shape) == (1, 8, 32, 32)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), layout="constrained")
    axes[0].imshow(rgb)
    axes[0].set_title("RGB blocks")
    axes[1].imshow(gray, cmap="gray", vmin=0, vmax=1)
    axes[1].set_title("Channel average")
    bound = max(abs(edge.min()), abs(edge.max()))
    shown = axes[2].imshow(edge, cmap="coolwarm", vmin=-bound, vmax=bound)
    axes[2].set_title("Horizontal difference")
    for ax in axes:
        ax.set(xlabel="Column u", ylabel="Row v")
    fig.colorbar(shown, ax=axes[2], shrink=0.8)
    fig.savefig(folder / "edges.png", dpi=150)
    print(folder / "edges.png")
