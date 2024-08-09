#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>

#define SPI_DEVICE "/dev/spidev0.0" // SPI device on Raspberry Pi

int main(void) {
    int spi_fd;
    uint8_t tx_buffer[] = {0xAA, 0x55, 0xFF, 0x00}; // Test data to send
    uint8_t rx_buffer[sizeof(tx_buffer)] = {0};     // Buffer to hold received data
    struct spi_ioc_transfer spi_transfer;
    int ret;

    uint8_t mode = SPI_MODE_0;             // SPI mode
    uint8_t bits = 8;                      // Bits per word
    uint32_t speed = 500000;               // Speed in Hz

    // Open the SPI device
    spi_fd = open(SPI_DEVICE, O_RDWR);
    if (spi_fd < 0) {
        perror("Failed to open SPI device");
        return EXIT_FAILURE;
    }

    // Set SPI mode
    ret = ioctl(spi_fd, SPI_IOC_WR_MODE, &mode);
    if (ret == -1) {
        perror("Failed to set SPI mode");
        close(spi_fd);
        return EXIT_FAILURE;
    }

    // Set bits per word
    ret = ioctl(spi_fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    if (ret == -1) {
        perror("Failed to set bits per word");
        close(spi_fd);
        return EXIT_FAILURE;
    }

    // Set SPI speed
    ret = ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
    if (ret == -1) {
        perror("Failed to set SPI speed");
        close(spi_fd);
        return EXIT_FAILURE;
    }

    // Prepare the SPI transfer structure
    memset(&spi_transfer, 0, sizeof(spi_transfer));
    spi_transfer.tx_buf = (unsigned long)tx_buffer;
    spi_transfer.rx_buf = (unsigned long)rx_buffer;
    spi_transfer.len = sizeof(tx_buffer);
    spi_transfer.speed_hz = speed;
    spi_transfer.bits_per_word = bits;

    // Perform the SPI transfer
    ret = ioctl(spi_fd, SPI_IOC_MESSAGE(1), &spi_transfer);
    if (ret < 0) {
        perror("Failed to perform SPI transfer");
        close(spi_fd);
        return EXIT_FAILURE;
    }

    // Compare sent and received data
    if (memcmp(tx_buffer, rx_buffer, sizeof(tx_buffer)) == 0) {
        printf("SPI loopback test passed!\n");
    } else {
        printf("SPI loopback test failed!\n");
        printf("Sent:    ");
        for (int i = 0; i < sizeof(tx_buffer); i++) {
            printf("0x%02X ", tx_buffer[i]);
        }
        printf("\nReceived: ");
        for (int i = 0; i < sizeof(rx_buffer); i++) {
            printf("0x%02X ", rx_buffer[i]);
        }
        printf("\n");
    }

    // Close the SPI device
    close(spi_fd);
    return EXIT_SUCCESS;
}