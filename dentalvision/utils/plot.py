'''
Create plots of particular stages of the project.
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.structure import Shape


PLOT_STAGES = False


def plot(choice, *args):
    '''
    Plot the different stages of the project. Set PLOT_STAGES to False
    to avoid plotting.
    '''
    if not PLOT_STAGES:
        return
    else:
        if choice == 'gpa':
            return plot_gpa(*args)
        elif choice == 'eigenvectors':
            return plot_eigenvectors(*args)
        elif choice == 'deformablemodel':
            return plot_deformablemodel(*args)


def plot_gpa(mean, aligned_shapes):
    '''
    Plot the result of GPA; plot the mean and the first 10 deviating shapes
    '''
    # plot mean
    mx, my = np.split(mean, 2)
    plt.plot(mx, my, color='r', marker='o')
    # plot first i aligned deviations
    for i in range(len(aligned_shapes)):
        a = aligned_shapes[i, :]
        ax, ay = np.split(a, 2)
        plt.scatter(ax, ay)
    axes = plt.gca()
    axes.set_xlim([-0.8, 0.8])
    plt.show()


def plot_eigenvectors(mean, eigenvectors):
    '''
    Plot the eigenvectors within a mean image.
    Centroid of mean must be the origin!
    '''
    mx, my = np.split(mean, 2)
    plt.plot(mx, my, marker='o')

    axes = plt.gca()
    axes.set_xlim([-0.8, 0.8])

    for i in range(6):
        vec = eigenvectors[:, i].T
        axes.arrow(0, 0, vec[0], vec[1], fc='k', ec='k')

    plt.show()


def plot_deformablemodel(model):
    z = np.zeros(60)

    # recreate the mean
    mode = model.deform(z)
    plt.plot(mode.x, mode.y)

    # create variations
    # for i in range(20):
    z[2] = 0.3
    z[1] = 0.1
    z[0] = 0
    var = model.deform(z)
    plt.plot(var.x, var.y, marker='o')

    axes = plt.gca()
    axes.set_xlim([-1, 1])
    axes.set_ylim([-0.5, 0.5])
    plt.show()


def render_shape(shape):
    if not isinstance(shape, Shape):
        shape = Shape(shape)
    plt.plot(shape.x, shape.y, marker='o')

    axes = plt.gca()
    # axes.set_xlim([-1, 1])
    # axes.set_ylim([-0.5, 0.5])
    plt.show()


def render_shape_to_image(shape):
    if not isinstance(shape, Shape):
        shape = Shape(shape)

    img = np.zeros((1600, 3000))
    color = (255, 255, 255)

    for i in range(shape.length - 1):
        cv2.line(img, (int(shape.x[i]), int(shape.y[i])),
            (int(shape.x[i + 1]), int(shape.y[i + 1])), color, 5)

    return img


def render_image(img, shape, color=None, title='Image'):
    '''
    Draw shape over image
    '''
    if not isinstance(shape, Shape):
        shape = Shape(shape)
    if color is None:
        color = (255, 0, 0)

    for i in range(shape.length - 1):
        cv2.line(img, (int(shape.x[i]), int(shape.y[i])),
            (int(shape.x[i + 1]), int(shape.y[i + 1])), color, 5)

    render(img)


def render_inits(img, matches, color=None, title='Inits'):
    for m in matches:
        cv2.ellipse(img, tuple(m), (50, 120), 0, 0, 360, (255, 0, 0), 5)
    render(img)


def render(img, title='img'):
    height = 600
    scale = height / float(img.shape[0])
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)

    cv2.namedWindow(str(title), cv2.WINDOW_NORMAL)
    cv2.resizeWindow(str(title), window_width, window_height)
    cv2.imshow(str(title), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()