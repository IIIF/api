module.exports = function(grunt) {
  grunt.initConfig({
    htmllint: {
        all: [
          '_site/**/*.html'
        ]
    }
  });
  grunt.loadNpmTasks('grunt-html');
  grunt.registerTask('test', ['htmllint']);
};
